import json
import operator
import time

import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse as time_parse

from Scraper.framework.components_basic import ComponentBasic

IMAGE_DATA_FIELD_TO_JSON_DATA_FIELD = {
    "image_id": "id",
    # image_links
    # image_parent_link

    # image_tags
    # image_extension
    "image_title":          "title",
    "image_type":           "illustType",
    "image_date":           "createDate",
    "image_uploader_id":    "userId",
    "image_uploader_name":  "userName",
    "image_width":          "width",
    "image_height":         "height",
    "image_page_count":     "pageCount",
    "image_bookmarks":      "bookmarkCount",
    "image_views":          "viewCount",
    "image_likes":          "likeCount",
    "image_comments":       "commentCount", # number of comments
    "image_is_original":    "isOriginal"
}

IMAGE_DATA_FIELD_TO_CONFIGURATION = {

}

class ComponentPixiv(ComponentBasic):
    api_endpoint = ("""
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

    artwork_view_url = "https://www.pixiv.net/artworks/{id}"

    # "&p={page}" is missing because it will not be formatted with user set configurations

    def __init__(self, init_verbose=True):
        super().__init__("pixiv.ini", init_verbose=init_verbose)

        self.url_as_referer = True
        # self.download_cookie    = {"PHPSESSID": self.config["phpsessid"]}
        # User-Agent Header will auto configure

        self.logger.info("Logging in to Pixiv")

    def generate_urls(self):  # TODO: Make tags_exclude_query actually work
        f_tags = self.config["tags_query"] + self.config["tags_exclude_query"]
        base_url_formatted = self.api_endpoint.format(f_tags=f_tags, **self.config.get_configuration())
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
                filtered_results.append(result["id"])

        image_data = []
        for result in filtered_results:
            self.logger.debug("Retriving extended data for image with id: {}".format(result))
            image_data.append(self.retrive_extended_data(result))

        return image_data

    def verify_requirements_basic(self, data: dict) -> bool:  # requirements that is
        if data["isAdContainer"]:
            self.logger.debug("Filter out submission due to it is an AD container")
            return False

        if self.config["ignore_bookmarked"] and not data["isBookmarkable"]:
            self.logger.debug(f"Filter out {data['id']} due to target is not bookmarkable, which probably because already bookmarked")
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

    def retrive_extended_data(self, img_id: str):  # bypass rate limiting (hopefully will work)
        r = requests.get(self.artwork_view_url.format(id=img_id))
        if r.status_code >= 400:
            self.logger.error(f"Error while getting artwork page. Status Code: {r.status_code}")
            return;

        bs = BeautifulSoup(r.content, "lxml", from_encoding=r.encoding)
        artwork_details = bs.find("meta", attrs={"id": "meta-preload-data"})
        artwork_details = json.loads(artwork_details.get("content"))
        return self.restructure_extended_data(artwork_details)

    def restructure_extended_data(self, data: dict):
        data = data["illust"][list(data["illust"].keys())[0]]
        image_data = {}
        for k, v in IMAGE_DATA_FIELD_TO_JSON_DATA_FIELD.items():
            image_data.update({k: data[v]})
        # Process tags
        tags_list = data["tags"]["tags"]
        tags_string = " ".join([i["tag"] for i in tags_list])
        image_data.update({"image_tags": tags_string})
        # Process links
        image_data.update({"image_parent_link": self.artwork_view_url.format(id=image_data["image_id"])})
        # do some math calculation
        image_data.update({"image_avg_bookmark_perday":
            self._calculate_avg_bookmark_per_day(image_data["image_date"], image_data["image_bookmarks"])})
        image_data.update({"image_view_bookmark_ratio":
            (data["image_views"] / data["image_bookmarks"])})

        extension = data["urls"][self.config["image_size"]].split(".")[-1]
        image_data.update({"image_extension": extension})
        # because the response only contains the direct link of the first image,
        # we have to make out rest of the image url
        base_url = data["urls"]["original"].replace("p0", "p{}")
        image_urls = [base_url.format(i) for i in range(0, image_data["image_page_count"])]
        image_data.update({"image_links": image_urls})
        return image_data

    def are_requirements_satisfied(self, data: dict):
        # Very easy to hit rate limit
        if not (self._calculate_avg_bookmark_per_day(data["image_date"], data["image_bookmarks"]) >=
                self.config["avg_bookmark_per_day"]):
            self.logger.debug(f"Filter out {data['image_id']} due to insufficient avg bookmark perday: {int(self._calculate_avg_bookmark_per_day(data['image_date'], data['image_bookmarks']))}")
            return False

        if not (data["image_views"] >= self.config["view_min"]):
            self.logger.debug(f"Filter out {data['image_id']} due to insufficient view counts: {data['image_views']}")
            return False

        # Check if the bookmark count matches requirements
        if not (data["image_bookmarks"] >= self.config["bookmark_min"]):
            self.logger.debug(f"Filter out {data['image_id']} due to insufficient bookmarks: {data['image_bookmarks']}")
            return False

        if not (int(data["image_views"] / data["image_bookmarks"]) >= self.config["view_bookmark_ratio"]):
            if data["image_bookmarks"] >= self.config["view_bookmark_ratio_bypass"] > 0:
                self.logger.debug(
                    f"Did not filter out {data['image_id']} even it's view/bookmark ratio did not meet requirement because it's total book mark {data['image_bookmarks']} triggered bypass")
            else:
                self.logger.debug(
                    f"Filter out {data['image_id']} due to insufficient view/bookmark ratio: {int(data['image_views'] / data['image_bookmarks'])}")
                return False

        return True

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
