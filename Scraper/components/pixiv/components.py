import json
import operator
import time

import requests
from dateutil.parser import parse as time_parse
from pixivpy3.aapi import AppPixivAPI

from Scraper.framework.components_basic import ComponentBasic


class ComponentPixiv(ComponentBasic):
    base_url = ("""
        https://www.pixiv.net/ajax/search/artworks/{f_tags}?word={f_tags}
                                                        &order={sorted_by}
                                                        &mode={rating}
                                                        &scd={submission_after}
                                                        &ecd={submission_before}
                                                        &s_mode={search_mode}
                                                        &type={submission_type}
                                                        &wlt={width_min}
                                                        &wgt={width_max}
                                                        &hlt={height_min}
                                                        &hgt={height_max}
                                                        &ratio={orientation}
                                                        &tool={tool}
    """.replace(" ", "").replace("\n", ""))  # Remove space and new lines because triple quote string will include those

    # Also "&p={page}" is missing because it will not be formatted with user set configurations

    def __init__(self, init_verbose=True):
        super().__init__("pixiv.ini", init_verbose=init_verbose)

        self.url_as_referer = True

        self.pixiv_app_api = AppPixivAPI()  # This will help us to get details about a specific submission

        # self.download_cookie    = {"PHPSESSID": self.config["phpsessid"]}
        # User-Agent Header will auto configure

        self.logger.info("Logging in to Pixiv")
        self.pixiv_app_api.login(self.config["username"], self.config["password"])

    def generate_urls(self):  # TODO: Make tags_exclude_query actually work
        f_tags = self.config["tags_query"] + self.config["tags_exclude_query"]
        base_url_formatted = self.base_url.format(f_tags=f_tags, **self.config.get_configuration())
        base_url_with_pg_number = base_url_formatted + "&p={page}"
        list_of_urls = [(base_url_with_pg_number.format(page=i), i) for i in
                        range(self.config["start_page"], (self.config["end_page"] + 1))]
        return list_of_urls

    def process_page(self, url: str):
        resp = requests.get(url, headers=self.request_header, cookies=self.request_cookie)
        api_resp = json.loads(resp.content)
        if resp.status_code >= 400:
            self.logger.error(f"Error while fetching search API Response: {api_resp}. E: {resp.status_code}")
            return;

        search_resp: list = api_resp["body"]["illustManga"]["data"]

        filtered_results = []

        for result in search_resp:
            if self.verify_requirements_basic(result):
                filtered_results.append(result)

        return filtered_results

    def verify_requirements_basic(self, data: dict) -> bool:
        if data["isAdContainer"]:
            self.logger.debug(f"Filter out submission due to it is an AD container")
            return False

        if self.config["ignore_bookmarked"] and not data["isBookmarkable"]:
            self.logger.debug(
                f"Filter out {data['id']} due to target is not bookmarkable, which assuming already bookmarked")
            return False

        # Check if user is not in our filtered list
        if data["userId"] in self.config["user_include"]:
            self.logger.debug(f"Accepted {data['id']} due to submitted by a user in user_include")
            return True
        if data["userId"] in self.config["user_exclude"]:
            self.logger.debug(f"Filter out {data['id']} due to submitted by a user in user_exclude")
            return False

        for include_kw in self.config["title_include"]:
            if include_kw not in data["title"]:
                self.logger.debug(
                    f"Filter out {data['id']} due to include keyword in title is not present. Keyword: {include_kw}")
                return False

        for exclude_kw in self.config["title_exclude"]:
            if exclude_kw in data["title"]:
                self.logger.debug(
                    f"Filter out {data['id']} due to exclude keyword in title is present. Keyword: {exclude_kw}")
                return False

        comp_operator = operator.eq if self.config["non_query_tag_match_mode"] == "absolute" else operator.contains

        for tag in data["tags"]:
            for excluded in self.config["tags_exclude"]:
                if comp_operator(excluded, tag):
                    self.logger.debug(f"Filter out {data['id']} due to exclude tag is present. Tag: {excluded}")
                    return False

            for bypass in self.config["tags_bypass"]:
                self.logger.debug(f"Accept {data['id']} due to bypass tag is present. Tag: {bypass}")
                if comp_operator(bypass, tag): return True

        for exclude_kw in self.config["description_exclude"]:
            if exclude_kw in data["description"]:
                self.logger.debug(
                    f"Filter out {data['id']} due to exclude keyword in description is present. Keyword: {exclude_kw}")
                return False

        if (self.config["page_count_min"] > data["pageCount"] and self.config["page_count_min"] > 0) or \
                (data["pageCount"] > self.config["page_count_max"] > 0):
            self.logger.debug(f"Filter out {data['id']} due to excluded min max page number")
            return False

        return True

    def are_requirements_satisfied(self, data: dict):
        details = self.pixiv_app_api.illust_detail(data["id"])[
            "illust"]  # get some extended infomation such as bookmark count and view count

        if not (self._calculate_avg_bookmark_per_day(details["create_date"], details["total_bookmarks"]) >=
                self.config["avg_bookmark_per_day"]):
            self.logger.debug(
                f"Filter out {data['id']} due to insufficient avg bookmark perday: {int(self._calculate_avg_bookmark_per_day(details['create_date'], details['total_bookmarks']))}")
            return False

        if not (details["total_view"] >= self.config["view_min"]):
            self.logger.debug(f"Filter out {details['id']} due to insufficient view counts: {details['total_view']}")
            return False

        # Check if the bookmark count matches requirements
        if not (details["total_bookmarks"] >= self.config["bookmark_min"]):
            self.logger.debug(f"Filter out {details['id']} due to insufficient bookmarks: {details['total_bookmarks']}")
            return False

        if not (int(details["total_view"] / details["total_bookmarks"]) <= self.config["view_bookmark_ratio"]):
            if details["total_bookmarks"] >= self.config["view_bookmark_ratio_bypass"] > 0:
                self.logger.debug(
                    f"Did not filter out {details['id']} even it's view/bookmark ratio did not meet requirement because it's total book mark {details['total_bookmarks']} triggered bypass")
            else:
                self.logger.debug(
                    f"Filter out {details['id']} due to insufficient view/bookmark ratio: {int(details['total_view'] / details['total_bookmarks'])}")
                return False

        self._restructure_image_data(data, details)

        return True

    def _restructure_image_data(self, org_data: dict, extra_data: dict):
        base_submission_url = "https://www.pixiv.net/artworks/{illustId}"

        extra_data_keys = [
            "id", "title", "type", "create_date", "page_count",
            "total_view", "total_bookmarks", "total_comments",
            "width", "height"
        ]

        org_data_keys = ["tags", "userId", "userName"]

        org_data_copy = org_data.copy()

        org_data.clear()  # clear the current content

        # Because dict is immutable we can update it's value cross the board
        # using the .update() method. do not assign as it is not pass by reference
        org_data.update({"image_parent_link": base_submission_url.format(illustId=extra_data["id"])})

        org_data.update({"image_id": extra_data["id"]})

        # Get list of direct link to the images to download
        img_raw_link = [img["image_urls"][self.config["image_size"]] for img in extra_data["meta_pages"]]
        org_data.update({"image_links": img_raw_link})

        for data_keys in extra_data_keys:
            org_data.update({data_keys: extra_data[data_keys]})

        for data_keys in org_data_keys:
            org_data.update({data_keys: org_data_copy[data_keys]})

    @staticmethod
    def _calculate_avg_bookmark_per_day(created_date: str, total_bookmark: int):
        current_JST_time = time.time() + 32400  # 32400 is 9 hours which is the JST offset from CST (Central Daylight Time), That is assuming you are in CST
        upload_time = time_parse(created_date).timestamp()  # parse the ISO-8601 Formmatted string to Unix Epoch
        days_passed = (
                              current_JST_time - upload_time) / 86400  # divide the difference between current time and upload time by a day
        bookmark_per_day = total_bookmark / days_passed
        return bookmark_per_day

    def exit(self, code=0):
        return super().exit_handler(code=code)

    @staticmethod
    def entry_point(scraper_framework_base):
        return super().entry_point(scraper_framework_base)
