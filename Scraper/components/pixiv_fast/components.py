import json
import operator
import time
from typing import Tuple

import requests
from dateutil.parser import parse as time_parse
from pixivpy3.aapi import AppPixivAPI

from Scraper.framework._components_basic import ComponentBasic


class ComponentPixivFast(ComponentBasic):
    pixiv_submission_base_link = "https://www.pixiv.net/artworks/{id}"

    def __init__(self, *args, **kwargs):
        super().__init__("pixiv_fast.ini", init_verbose=True, *args, **kwargs)

        self.logger.info("Logging in")
        self.pixiv_api = AppPixivAPI()
        self.pixiv_api.login(self.config["username"], self.config["password"])


    def generate_urls(self):
        return [(i * 30, i) for i in range(self.config["start_page"] - 1, self.config["end_page"] + 1)]


    def process_page(self, url):
        data = self.pixiv_api.search_illust(
            word=self.config["tags"],
            search_target=self.config["search_mode"],
            sort=self.config["sorted_by"],
            duration=self.config["time_span"],
            offset=url
        )
        return self._restructure_image_data(data)


    def are_requirements_satisfied(self, img_data: dict):
        # Check of extra tag requirements
        for tag in img_data["tags"]:
            if tag in self.config["tags_bypass"]:
                self.logger.debug(f"Accepted {img_data['id']} due to tag bypass: {tag}");
                return True

            if tag in self.config["tags_exclude"]:
                self.logger.debug(f"Accepted {img_data['id']} due to tag exclude: {tag}");
                return False

        # Check if illust type requirements match
        if self.config["illust_type"] and (img_data["type"] not in self.config["illust_type"]):
            self.logger.debug(f"Filter out {img_data['id']} due to excluded illust type: {img_data['type']}")
            return False

        if not (self.calculate_avg_bookmark_per_day(img_data) >= self.config["avg_bookmark_per_day"]):
            self.logger.debug(f"Filter out {img_data['id']} due to insufficient avg bookmark perday: {int(self.calculate_avg_bookmark_per_day(img_data))}")
            return False

        if not (img_data["total_view"] >= self.config["view_min"]):
            self.logger.debug(f"Filter out {img_data['id']} due to insufficient view counts: {img_data['total_view']}")
            return False

        # Check if the bookmark count matches requirements
        if not (img_data["total_bookmarks"] >= self.config["bookmark_min"]):
            self.logger.debug(f"Filter out {img_data['id']} due to insufficient bookmarks: {img_data['total_bookmarks']}")
            return False

        if not (int(img_data["total_view"] / img_data["total_bookmarks"]) <= self.config["view_bookmark_ratio"]):
            if (img_data["total_bookmarks"] >= self.config["view_bookmark_ratio_bypass"]):
                self.logger.debug(f"Did not filter out {img_data['id']} even it's view/bookmark ratio did not meet requirement because it's total book mark {img_data['total_bookmarks']} triggered bypass")
            else:
                self.logger.debug(f"Filter out {img_data['id']} due to insufficient view/bookmark ratio: {int(img_data['total_view'] / img_data['total_bookmarks'])}")
                return False

        return True


    def _restructure_image_data(self, org_data: list):
        data = []

        exposed_keys = [
            "title", "type", "create_date", "page_count",
            "width", "height", "series", "total_view", "total_bookmarks",
            "is_bookmarked", "is_muted"
        ]

        for submission in org_data["illusts"]:
            submission_data = {}

            submission_data.update({"image_id": submission["id"]})
            submission_data.update({"image_parent_link": self.pixiv_submission_base_link.format(id=submission["id"])})

            for keys in exposed_keys:
                submission_data.update({keys: submission[keys]})

            tags = [tag["name"] for tag in submission["tags"]]

            submission_data.update({"user_id": submission["user"]["id"]})
            submission_data.update({"user_name": submission["user"]["name"]})
            submission_data.update({"user_followed": submission["user"]["is_followed"]})

            try:
                if (submission["meta_single_page"]):
                    submission_data.update({"image_links": [submission["meta_single_page"]["original_image_url"]]})
            except KeyError: pass

            try:
                submission_data["image_links"]
            except KeyError:
                direct_links = [img["image_urls"][self.config["image_size"]] for img in submission["meta_pages"]]
                submission_data.update({"image_links": direct_links})

            # if submission.__contains__("meta_single_page"): # sometimes the response will contain both meta_single_page and meta_pages
            #     submission_data.update({"image_links": [submission["meta_single_page"]["original_image_url"]]})
            # else:
            #     direct_links = [img["image_urls"][self.config["image_size"]] for img in submission["meta_pages"]]
            #     submission_data.update({"image_links": direct_links})
            # if (not submission_data.__contains__("image_links")) or (submission_data["image_link"]):
            #     self.logger.warning("Failed to gather direct link to image contained in post id: {}. Ignoring".format(submission_data["image_id"]))
            #     continue
            data.append(submission_data)
        return data


    @staticmethod
    def _calculate_avg_bookmark_per_day(created_date: str, total_bookmark: int):
        current_JST_time = time.time() + 32400  # 32400 is 9 hours which is the JST offset from CST (Central Daylight Time), That is assuming you are in CST
        upload_time = time_parse(created_date).timestamp()  # parse the ISO-8601 Formmatted string to Epoch
        days_passed = (current_JST_time - upload_time) / 86400  # divide the difference between current time and upload time by a day
        bookmark_per_day = total_bookmark / days_passed
        return bookmark_per_day
