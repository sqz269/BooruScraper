from Scraper.framework.components_basic import ComponentBasic
from typing import Tuple, List, Union

from bs4 import BeautifulSoup
from bs4.element import Tag
import requests


class MatchMode:
    INCLUDE = 0
    EXCLUDE = 1

    GREATER = 2
    SMALLER = 3
    EQUAL = 4

    # VARY    = 5


# Intresting Request: https://danbooru.donmai.us/posts/{PID}?variant=tooltip&preview=false
class ComponentsDanbooru(ComponentBasic):
    base_url = "https://danbooru.donmai.us/posts?page={page}&tags={tag}"
    base_submission_url = "https://danbooru.donmai.us/posts/{id}"

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
    };

    IMAGE_DATA_FIELD_TO_CONFIGURATION = {
        # WARNING: EXPERIMENTAL
        # Config name           : img_data[key]   value type  Compairson mode
        "tags_extra": ["image_tags", list, MatchMode.INCLUDE],
        "tags_exclude_extra": ["image_tags", list, MatchMode.EXCLUDE],

        # "rating"                : ["image_rating",      int,  MATCH_MODE.VARY   ],
        "children": ["image_has_children", bool, MatchMode.EQUAL],

        "extension": ["image_extension", list, MatchMode.INCLUDE],
        "extension_exclude": ["image_extension", list, MatchMode.EXCLUDE],

        "max_width": ["image_width", int, MatchMode.SMALLER],
        "min_width": ["image_width", int, MatchMode.GREATER],
        "max_height": ["image_height", int, MatchMode.SMALLER],
        "min_height": ["image_height", int, MatchMode.GREATER],

        "min_fav_count": ["image_fav_count", int, MatchMode.GREATER],
        "min_score": ["image_score", int, MatchMode.GREATER],

        "source_origin": ["image_source", list, MatchMode.INCLUDE],
        "source_origin_exclude": ["image_source", list, MatchMode.EXCLUDE]
    }

    def __init__(self, *args, **kwargs):
        # See _base_component->BaseComponent's constructor for argument details
        super().__init__("danbooru.ini", init_verbose=True)
        self.config.cvt_str_list(["tags_extra", "tags_exclude_extra"])

    def generate_urls(self) -> List[Tuple[str, str]]:
        tags: list = self.config["tags"].split(" ")
        tags_exclude: list = self.config["tags_exclude"].split(" ")

        # Optimise query: If tags query exceeds amount of tags you can put,
        # move them out of the query and check them individually in are_requirements_satisfied
        if len(tags) > 2:
            self.logger.warn(
                f"tags in tags will exceed 2 tag query limit; Moving tags out of query into non-query checking")
            self.config["tags_extra"].extend(tags[2:len(tags)])

        if len(tags) + len(tags_exclude) > 2:
            self.logger.warn(
                f"tags in tags_exclude will exceed 2 tag query limit; Moving tags out of query into non-query checking")
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
            img_data.update({"image_links": [post.get("data-file-url")]})
            img_data.update({"image_parent_link": self.base_submission_url.format(id=img_data["image_id"])})
            image_data_all.append(img_data)
        return image_data_all

    def automated_requirements_verification(self, data_to_config_dict: dict, data_dict: dict,
                                            short_circut=False) -> list:
        requirements_missed = []
        for k, v in data_to_config_dict.items():
            if not self._validate_requirement(self.config[k], data_dict[v[0]], v[1], v[2]):
                if short_circut: return [k]
                requirements_missed.append(k)
        return requirements_missed

    def _validate_requirement(self, standard_value, value, v_type: Union[int, str, list, bool],
                              mode: MatchMode) -> bool:
        if isinstance(v_type, int):
            if mode == MatchMode.EXCLUDE or mode == MatchMode.INCLUDE:
                self.logger.error(f"Unsupported matchmode of [EXCLUDE, INCLUDE] for type int")
                return False

            if MatchMode.EQUAL:
                self.logger.debug("Standard value: {}")
                return standard_value == value

            if MatchMode.GREATER:
                return standard_value > value

            if MatchMode.SMALLER:
                return standard_value < value

        if isinstance(v_type, str):
            if mode == MatchMode.GREATER or mode == MatchMode.SMALLER:
                self.logger.error(f"Unsupported matchmode of [GREATER, SMALLER] for type str")
                return False

            if MatchMode.EQUAL:
                return standard_value == value

            if MatchMode.INCLUDE:
                return standard_value in value  # TODO: Reverse compairson or something like that

            if MatchMode.EXCLUDE:
                return standard_value not in value

        if isinstance(v_type, bool):
            if mode == MatchMode.GREATER or mode == MatchMode.SMALLER or mode == MatchMode.EXCLUDE or mode == MatchMode.INCLUDE or mode == MatchMode.VARY:
                self.logger.error(
                    f"Unsupported matchmode of [GREATER, SMALLER, EXCLUDE, INCLUDE, VARY] for type bool. Only mode Equal is supported")
                return False

            return standard_value == value

        if isinstance(v_type, list):
            if mode == MatchMode.GREATER or mode == MatchMode.SMALLER or mode == MatchMode.VARY or mode == MatchMode.EQUAL:
                self.logger.error(f"Unsupported matchmode of [GREATER, SMALLER, VARY, EQUAL] for type list")
                return False

            if mode == MatchMode.INCLUDE:
                for elements in standard_value:
                    if not (elements in value): return False
                return True

            if mode == MatchMode.EXCLUDE:
                for elements in standard_value:
                    if (elements in value): return False
                return True

            # if mode == MATCH_MODE.EQUAL:

    def are_requirements_satisfied(self, data) -> bool:
        is_satisfied = self.automated_requirements_verification(self.IMAGE_DATA_FIELD_TO_CONFIGURATION, data, False)
        if not is_satisfied:
            self.logger.debug(f"Requirements were not satisfied due to fields: {is_satisfied}")
        return is_satisfied

    def entry_point(self, scraper_framework_base):
        return super().entry_point(scraper_framework_base)
