from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from Scraper.framework.i_components import IComponents
from Scraper.framework.base_component import BaseComponent

# TODO: Fix a problem where config {tags} used in master dir string
# will be presented in the form of a list instead of expected string


class ComponentGelbooru(BaseComponent, IComponents):
    BASE_URL = "https://gelbooru.com/index.php?page=post&s=list&tags={tag}&pid={page}"
    IMAGES_PER_PAGE = 42

    def __init__(self, config_path: str = None, config_dict: dict = None, load_config_from_abs_path=False, init_verbose=False):
        if config_path or config_path:
            super(ComponentGelbooru, self).__init__(config_path, config_dict, load_config_from_abs_path, init_verbose)
        else:
            super().__init__("gelbooru.ini", init_verbose)
        self.config.cvt_str_list(["tags", "tags_exclude"])

    def _construct_query(self) -> str:
        tags_include = ("+".join(self.config["tags"]))
        tags_exclude = ("+".join("-" + i for i in self.config["tags_exclude"]))

        rating = ""
        if (self.config["rating"] and self.config["rating_exclude"]):
            self.logger.warning("Both \"rating\" and \"rating_exclude\" are specified. but only one can exist. Using \"rating_exclude\"")
            rating = f"-rating:{self.config['rating_exclude']}"
        else:
            if (self.config["rating"]):
                rating = f"rating:{self.config['rating']}"
            elif (self.config["rating_exclude"]):
                rating = f"rating:{self.config['rating_exclude']}"
        query_terms = "+".join(i for i in [tags_exclude, tags_include, rating] if i)
        self.logger.debug(f"Constructed query: {query_terms}")
        return query_terms

    def generate_urls(self):
        # Urls page number increment by 42 and that's because there is 42 image on a page
        tags = self._construct_query()
        return [(self.BASE_URL.format(tag=tags, page=i * self.IMAGES_PER_PAGE), str(i)) for i in range(self.config["start_page"], self.config["end_page"])]

    def _predict_highres_url(self, org_url: str, tags: str) -> str:
        video_kw = ["webm", "animated"]
        is_video = False
        for kw in video_kw:
            if kw in tags:
                is_video = True;

        # build the base url w/o the image extension
        url = urlparse(org_url)
        url_path = url.path
        # URL path look like this: '/thumbnails/[first 2 char hash]/[last 2 char hash]/thumbnail_[full_hash].jpg
        image_hash = url_path.split("/")[-1].split("_")[-1].split(".")[0]
        # scheme://subdomain.domain.tld//images/[first 2 char of hash]/[2-4 char of hash]/[full hash].[file ext]
        image_org_path = f"{url.scheme}://{url.netloc}//images/{image_hash[0:2]}/{image_hash[2:4]}/{image_hash}"

        # Guess the file extension
        ext = [".mp4"] if is_video else [".jpg", ".png"]

        for extension in ext:
            full_url = image_org_path + extension
            # Checks if URL is available by sending a HEAD request (if not, try another extension)
            # so it doesn't cost that much resource for the server to respond
            r = requests.head(full_url, headers=self.request_header)
            if r.status_code <= 400:
                return (full_url, extension)
            self.logger.debug("Original image did not have file extension type: {}".format(extension))
        self.logger.warning("Failed to find an applicable file extension for image with original url: {}. Ignoring".format(org_url))
        return ("", "")

    def _extract_img_data(self, web_data: bytes, encoding="utf-8") -> list:
        bs = BeautifulSoup(web_data, "lxml", from_encoding=encoding)
        parent_base_url = "https://gelbooru.com/index.php?page=post&s=view&id={id}"

        image_data = []
        img = bs.find_all("img", attrs={"class": "thumbnail-preview"})
        for elem in img:
            img_id = elem["alt"].split(": ")[1]

            # Extract some infomation from title attribute
            # Title attribute look like this: "[tags (space separated)] score:[score] rating:[rating]"
            image_title = elem["title"].split(" ")  # The title element contains tags, rating and score
            image_title = [i for i in image_title if i]  # remove empty element from array
            image_rating = image_title[-1].split(":")[-1]
            image_score = int(image_title[-2].split(":")[-1])
            image_tags = " ".join(image_title[0:image_title.__len__() - 2])

            # Get image's highres url
            image_url, image_extension = self._predict_highres_url(elem["src"], image_tags)
            if not image_url: continue
            img_data = {
                "image_id": img_id,
                "image_links": [image_url],
                "image_parent_link": parent_base_url.format(id=img_id),

                "image_score": image_score,
                "image_tags": image_tags,
                "image_rating": image_rating,
                "image_extension": image_extension
            }
            image_data.append(img_data)
        return image_data

    def process_page(self, url: str):
        r = requests.get(url, headers=self.request_header)
        if (r.status_code >= 400):
            self.logger.error(f"Failed to fetch content from remote. Server returned status: {r.status_code}")

        return self._extract_img_data(r.content, r.encoding)

    def are_requirements_satisfied(self, data: dict):
        if data["image_score"] < self.config["min_score"]:
            return False
        return True
