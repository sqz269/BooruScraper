from typing import Tuple, List

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from Scraper.framework.base_component import MatchMode
from Scraper.framework.components_basic import ComponentBasic


class ComponentsDanbooru(ComponentBasic):
    base_url = "https://danbooru.donmai.us/posts?page={page}&tags={tag}"
    base_submission_url = "https://danbooru.donmai.us/posts/{id}"

    RATING_CHAR_TO_INT = {
        "r": 2,
        "e": 2,
        "q": 1,
        "s": 0
    }

    IMAGE_DATA_FIELD_TO_HTML_DATA_FIELD = {
        # required fields
        "image_id": "id",
        # some required fields require extra steps so it's not present here

        # requirements matching fields
        "image_tags": "tags",
        "image_rating": "rating",
        "image_width": "width",
        "image_height": "height",
        "image_flags": "flags",  # idk wtf is this
        "image_has_children": "has-children",
        "image_score": "score",
        "image_fav_count": "fav-count",
        "image_extension": "file-ext",
        "image_source": "normalized-source"
    }

    IMAGE_DATA_FIELD_TO_CONFIGURATION = {
        # WARNING: EXPERIMENTAL
        # Config name           : img_data[key]   value type  Compairson mode
        "tags_extra": ["image_tags", list, MatchMode.INCLUDE, " "],
        "tags_exclude_extra": ["image_tags", list, MatchMode.EXCLUDE, " "],

        # "rating"                : ["image_rating",      int,  MATCH_MODE.VARY],
        "children": ["image_has_children", bool, MatchMode.EQUAL],

        "extension": ["image_extension", list, MatchMode.SUPER_INCLUDE, " "],
        "extension_exclude": ["image_extension", list, MatchMode.SUPER_EXCLUDE, " "],

        "max_width": ["image_width", int, MatchMode.GREATER],
        "min_width": ["image_width", int, MatchMode.SMALLER],
        "max_height": ["image_height", int, MatchMode.GREATER],
        "min_height": ["image_height", int, MatchMode.SMALLER],

        "min_fav_count": ["image_fav_count", int, MatchMode.SMALLER],  # image_fav_count smaller than min_fav_count?
        "min_score": ["image_score", int, MatchMode.SMALLER],

        "source_origin": ["image_source", list, MatchMode.SUPER_INCLUDE, " "],
        "source_origin_exclude": ["image_source", list, MatchMode.SUPER_EXCLUDE, " "]
    }

    def __init__(self, *args, **kwargs):
        # See _base_component->BaseComponent's constructor for argument details
        super().__init__("danbooru.ini")
        self.config.cvt_str_list(["tags_extra", "tags_exclude_extra"])

    def generate_urls(self) -> List[Tuple[str, str]]:
        tags: list = self.config["tags"].split(" ")
        tags_exclude: list = self.config["tags_exclude"].split(" ")

        tags = [i for i in tags if i]
        tags_exclude = [i for i in tags_exclude if i]  # Remove empty elements

        # Optimise query: If tags query exceeds amount of tags you can put,
        # move them out of the query and check them individually in are_requirements_satisfied
        if len(tags) > 2:
            self.logger.warning(
                "tags in tags will exceed 2 tag query limit; Moving tags out of query into non-query checking")
            self.config["tags_extra"].extend(tags[2:len(tags)])

        if len(tags) + len(tags_exclude) > 2:
            self.logger.warning(
                "tags in tags_exclude will exceed 2 tag query limit; Moving tags out of query into non-query checking")
            self.config["tags_exclude_extra"].extend(tags_exclude[2:len(tags_exclude)])

        # joins the tags and exclude tags into one query string
        # the list comprehension is needed to add "-" in front of exclude tags
        # nasty trick with "or" utilizing it's behavior of returning second paramater if the first one is false
        # https://en.wikipedia.org/wiki/Short-circuit_evaluation
        tags_query_string = "+".join((tags.extend(["-" + i for i in tags_exclude]) or tags))

        return [(self.base_url.format(page=str(i), tag=tags_query_string), str(i)) for i in
                range(self.config["start_page"], self.config["end_page"] + 1)]

    def process_page(self, url: str) -> List[dict]:
        r = requests.get(url, headers=self.request_header)
        if (r.status_code >= 400):
            self.logger.error(f"Failed to get page: {url}. ErrorNo: {r.status_code}")
            return;

        bs = BeautifulSoup(r.content, "lxml")
        return self.extract_image_data(bs)

    def extract_image_data(self, bs: BeautifulSoup) -> List[dict]:
        image_data_all = []
        post_div: Tag = bs.find("div", attrs={"id": "posts-container"})
        for post in post_div.find_all("article"):
            img_data = {}
            for k, v in self.IMAGE_DATA_FIELD_TO_HTML_DATA_FIELD.items():
                img_data.update({k: post.get(f"data-{v}")})
            img_data.update({"image_links": [
                post.get("data-file-url")]})  # image links need to be a list so it can't be automatically updated
            img_data.update({"image_parent_link": self.base_submission_url.format(id=img_data["image_id"])})
            image_data_all.append(img_data)
        return image_data_all

    def are_requirements_satisfied(self, data: dict) -> bool:
        unsatisfied_fields = self.automated_requirements_verification(self.IMAGE_DATA_FIELD_TO_CONFIGURATION, data,
                                                                      False)
        if unsatisfied_fields:
            self.logger.debug(f"Requirements were not satisfied due to fields: {unsatisfied_fields}")
            return False

        # check rating requirements due to it's dependency on another configuration: RATING_CHECK_STRICT
        if self.config["rating_check_strict"]:
            return data["image_rating"] == self.config["rating"]
        else:
            return self.RATING_CHAR_TO_INT[self.config["rating"]] >= self.RATING_CHAR_TO_INT[data["image_rating"]]

    def entry_point(self, scraper_framework_base):
        return super().entry_point(scraper_framework_base)
