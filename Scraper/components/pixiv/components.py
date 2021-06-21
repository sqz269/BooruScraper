import json
import operator
import time
from urllib.parse import quote_plus as url_quote

import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse as time_parse

from Scraper.framework.base_component import BaseComponent
from Scraper.framework.i_components import IComponents

IMAGE_DATA_FIELD_TO_JSON_DATA_FIELD = {
    "image_id": "id",
    # image_links
    # image_parent_link

    # image_tags
    # image_extension
    "image_title": "title",
    "image_type": "illustType",
    "image_date": "createDate",
    "image_uploader_id": "userId",
    "image_uploader_name": "userName",
    "image_width": "width",
    "image_height": "height",
    "image_page_count": "pageCount",
    "image_bookmarks": "bookmarkCount",
    "image_views": "viewCount",
    "image_likes": "likeCount",
    "image_comments": "commentCount",  # number of comments
    "image_is_original": "isOriginal"
}

class PreverifyState:
    FAILED = 0
    BYPASSED = 1
    PASSED = 2

class ComponentPixiv(BaseComponent, IComponents):
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
        """.replace(" ", "").replace("\n",
                                     ""))  # Remove space and new lines because triple quote string will include those

    artwork_view_url = "https://www.pixiv.net/artworks/{id}"

    # "&p={page}" is missing because it will not be formatted with user set configurations

    def __init__(self, config_path: str = None, config_dict: dict = None, load_config_from_abs_path=False,
                 init_verbose=False):
        if config_path or config_dict:
            super(ComponentPixiv, self).__init__(config_path, config_dict, load_config_from_abs_path, init_verbose)
        else:
            super().__init__("pixiv.ini", init_verbose=init_verbose)
        self.request_cookie = {"PHPSESSID": self.config["phpsessid"]}
        self.url_as_referer = True
        # User-Agent Header will auto configure

        try:
            int(self.config["avg_bookmark_per_day"])
        except ValueError:
            # because we are using eval to calculate the math expression, which allows custom code to execute
            self.logger.warning(
                "Using a custom expression for avg_bookmark_per_day may have unintended side effects. Proceed with caution.")

    def generate_urls(self):  # TODO: Make tags_exclude_query actually work
        f_tags = self.config["tags_query"] + self.config["tags_exclude_query"]
        base_url_formatted = self.api_endpoint.format(f_tags=f_tags, **self.config.get_configuration())
        base_url_with_pg_number = base_url_formatted + "&p={page}"
        list_of_urls = [(base_url_with_pg_number.format(page=i), i) for i in
                        range(self.config["start_page"], (self.config["end_page"] + 1))]
        return list_of_urls

    def _fill_data_bypass(self, image_data: dict) -> dict:
        link_org_template = "https://i.pximg.net/img-original/{data}"
        if "custom-thumb" in image_data["url"]:
            link_path = image_data["url"].split("custom-thumb/")[-1].replace("p0_custom1200", "{}")
        elif "img-master" in image_data["url"]:
            link_path = image_data["url"].split("img-master/")[-1].replace("p0_square1200", "{}")
        else:
            self.logger.warn("Bruh")
            breakpoint()

        link_path = link_path.replace(".jpg", ".png")
        org_link_template = link_org_template.format(data=link_path)
        links = [org_link_template.format(f"p{i}") for i in range(0, image_data["pageCount"])]

        template = {
            'image_id': image_data["id"], 
            'image_title': image_data["title"], 
            'image_type': image_data["illustType"], 
            'image_date': image_data["createDate"], 
            'image_uploader_id': image_data["userId"], 
            'image_uploader_name': image_data["userName"], 
            'image_width': image_data["width"], 
            'image_height': image_data["height"], 
            'image_page_count': image_data["pageCount"], 
            'image_bookmarks': -1, 
            'image_views': -1, 
            'image_likes': -1, 
            'image_comments': -1, 
            'image_is_original': None,
            'image_tags': "".join(image_data['tags']),
            'image_parent_link': self.artwork_view_url.format(id=image_data["id"]),
            'image_avg_bookmark_perday': -1,
            'image_view_bookmark_ratio': -1,
            'image_extension': image_data["url"].split(".")[-1],
            'image_links': links,
            'use_bypass': True
        }
        
        return template

    def process_page(self, url: str):
        self.logger.debug(f"Processing url: {url}")
        resp = requests.get(url, headers=self.request_header, cookies=self.request_cookie)
        api_resp = json.loads(resp.content)
        if resp.status_code >= 400:
            self.logger.error(f"Error while fetching search API Response: {api_resp}. E: {resp.status_code}")
            return;

        search_resp: list = api_resp["body"]["illustManga"]["data"]

        filtered_results = []
        bypass_results = {}
        for result in search_resp:
            req = self.verify_requirements_basic(result)
            if req == PreverifyState.FAILED:
                continue;
            elif req == PreverifyState.PASSED:
                filtered_results.append(result["id"])
            else:
                bypass_results.update({result['id']: result})

        image_data = []
        for data in bypass_results.values():
            image_data.append(self._fill_data_bypass(data))

        for result in filtered_results:
            self.logger.debug("Retriving extended data for image with id: {}".format(result))
            image_data.append(self.retrive_extended_data(result))

        return image_data

    def verify_requirements_basic(self, data: dict) -> PreverifyState:  # requirements that is
        if data.get("isAdContainer", False):
            return PreverifyState.FAILED

        if self.config["ignore_bookmarked"] and not data["isBookmarkable"]:
            self.logger.debug(
                f"Filter out {data['id']} due to target is not bookmarkable, which probably because already bookmarked")
            return PreverifyState.FAILED

        # Check if user is not in our filtered list
        if data["userId"] in self.config["user_include"]:
            self.logger.debug(f"Accepted {data['id']} due to submitted by a user in user_include")
            return PreverifyState.BYPASSED
        if data["userId"] in self.config["user_exclude"]:
            self.logger.debug(f"Filter out {data['id']} due to submitted by a user in user_exclude")
            return PreverifyState.FAILED

        for include_kw in self.config["title_include"]:
            if include_kw not in data["title"]:
                self.logger.debug(
                    f"Filter out {data['id']} due to include keyword in title is not present. Keyword: {include_kw}")
                return  PreverifyState.FAILED

        for exclude_kw in self.config["title_exclude"]:
            if exclude_kw in data["title"]:
                self.logger.debug(
                    f"Filter out {data['id']} due to exclude keyword in title is present. Keyword: {exclude_kw}")
                return PreverifyState.FAILED

        comp_operator = operator.eq if self.config["non_query_tag_match_mode"] == "absolute" else operator.contains

        for tag in data["tags"]:
            for excluded in self.config["tags_exclude"]:
                if comp_operator(excluded, tag):
                    self.logger.debug(f"Filter out {data['id']} due to exclude tag is present. Tag: {excluded}")
                    return PreverifyState.FAILED

            for bypass in self.config["tags_bypass"]:
                self.logger.debug(f"Accept {data['id']} due to bypass tag is present. Tag: {bypass}")
                if comp_operator(bypass, tag):
                    return PreverifyState.BYPASSED

        for exclude_kw in self.config["description_exclude"]:
            if exclude_kw in data["description"]:
                self.logger.debug(
                    f"Filter out {data['id']} due to exclude keyword in description is present. Keyword: {exclude_kw}")
                return PreverifyState.FAILED

        if (self.config["page_count_min"] > data["pageCount"] and self.config["page_count_min"] > 0) or \
                (data["pageCount"] > self.config["page_count_max"] > 0):
            self.logger.debug(f"Filter out {data['id']} due to excluded min max page number")
            return PreverifyState.FAILED

        return PreverifyState.PASSED

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
        tags_string = " ".join(i["tag"] for i in tags_list)
        image_data.update({"image_tags": tags_string})
        # Process links
        image_data.update({"image_parent_link": self.artwork_view_url.format(id=image_data["image_id"])})
        # do some math calculation
        image_data.update({"image_avg_bookmark_perday":
                               self._calculate_avg_bookmark_per_day(image_data["image_date"],
                                                                    image_data["image_bookmarks"])[0]}) # calc_avg_bookmark return a tuple (avg_bookmark_perday, days_passed)

        if image_data["image_bookmarks"] != 0:  # prevent 0 division error
            image_data.update({"image_view_bookmark_ratio":
                                   (image_data["image_views"] / image_data["image_bookmarks"])})
        else:
            image_data["image_view_bookmark_ratio"] = 0

        extension = data["urls"][self.config["image_size"]].split(".")[-1]
        image_data.update({"image_extension": extension})
        # because the response only contains the direct link of the first image,
        # we have to make out rest of the image url
        base_url = data["urls"]["original"].replace("p0", "p{}")
        image_urls = [base_url.format(i) for i in range(0, image_data["image_page_count"])]  # TODO: Should this field only contain one url?
        image_data.update({"image_links": image_urls})
        image_data.update({"use_bypass": False})
        return image_data

    def are_requirements_satisfied(self, data: dict):
        if data["use_bypass"]:
            self.logger.debug(f"Accpted {data['image_id']} due to use_bypass")
            return True

        avg_booksmarks, days_passed = self._calculate_avg_bookmark_per_day(data["image_date"], data["image_bookmarks"])
        if not (avg_booksmarks >= self.math_eval(self.config["avg_bookmark_per_day"], local_var={"t": days_passed})):
            self.logger.debug(
                f"Filter out {data['image_id']} due to insufficient avg bookmark perday: {self.math_eval(self.config['avg_bookmark_per_day'], local_var={'t': days_passed})}")
            return False

        if not (data["image_views"] >= self.config["view_min"]):
            self.logger.debug(f"Filter out {data['image_id']} due to insufficient view counts: {data['image_views']}")
            return False

        # Check if the bookmark count matches requirements
        if not (data["image_bookmarks"] >= self.config["bookmark_min"]):
            self.logger.debug(f"Filter out {data['image_id']} due to insufficient bookmarks: {data['image_bookmarks']}")
            return False

        try:
            if not (int(data["image_views"] / data["image_bookmarks"]) >= self.config["view_bookmark_ratio"]):
                if data["image_bookmarks"] >= self.config["view_bookmark_ratio_bypass"] > 0:
                    self.logger.debug(
                        f"Did not filter out {data['image_id']} even it's view/bookmark ratio did not meet requirement because it's total book mark {data['image_bookmarks']} triggered bypass")
                else:
                    self.logger.debug(
                        f"Filter out {data['image_id']} due to insufficient view/bookmark ratio: {int(data['image_views'] / data['image_bookmarks'])}")
                    return False
        except ZeroDivisionError:
            return False  # this should already be guarded with config BOOKMARK_MIN

        return True

    @staticmethod
    def _calculate_avg_bookmark_per_day(created_date: str, total_bookmark: int):
        current_JST_time = time.time()  # possibility of timezone offsets
        upload_time = time_parse(created_date).timestamp()  # parse the ISO-8601 Formmatted string to Unix Epoch
        days_passed = (current_JST_time - upload_time) / 86400  # Convert seconds to days
        bookmark_per_day = total_bookmark / days_passed
        return (bookmark_per_day, days_passed)

    def exit(self, code=0):
        return super().exit_handler(code=code)

    @staticmethod
    def entry_point(scraper_framework_base):
        return super().entry_point(scraper_framework_base)
