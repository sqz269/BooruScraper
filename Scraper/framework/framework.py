import os
import time
from concurrent.futures.thread import ThreadPoolExecutor
from typing import BinaryIO, List, Tuple

from Scraper.framework.components_basic import ComponentBasic


def init_scraper_base(SuperClass: ComponentBasic, *args, **kwargs):
    """Initializes a class instance of ScraperBase with SuperClass (parameter) as it's superclass

    Arguments:
        SuperClass {ComponentBasic} -- The super class ScraperBase will be inheriting from, should be a child class of ComponentBasic
                                        !!! The child class of ComponentBasic should override all it's methods in-order for it to work

    Returns:
        ScraperBase -- An initalized instance of ScraperBase that is inheriting SuperClass (param)
    """
    print(f"[*] Using class: {SuperClass.__name__}. With SuperClass: {SuperClass.__bases__}")

    # assert ComponentBasic in SuperClass.__base__, f"Class {type(SuperClass).__name__} has to be a sub class of ComponentBasic at Scraper.framework._components_basic"
    class ScraperBase(SuperClass):

        def __init__(self, *args, **kwargs):
            self.master_directory: str = None
            self.directory_created: list = []
            self.csv_io: BinaryIO = None

            super().__init__(*args, **kwargs)

        def run(self):
            """executes the scraper
            """
            self.logger.info("Preparing folders and files")
            self.initialize_file_and_directory()

            self.logger.debug("Generating list of urls that will be scraped")
            urls = self.generate_urls()
            if (self.config["reverse_generated_url"]):
                self.logger.debug("Reversing generated url")
                urls = urls[::-1]

            if (self.config["max_concurrent_thread"] > 5):
                self.logger.warning("Max conccurent thread exceeds 5, some server might issue temp ban on your ip")

            with ThreadPoolExecutor(max_workers=self.config["max_concurrent_thread"],
                                    thread_name_prefix=self.config["thread_name_prefix"]) as executor:
                for url in urls:
                    self.logger.debug(f"Queuing url: {url[0]} for processing")
                    executor.submit(self._start, url)
                self.logger.info(
                    f"Queued {len(urls)} urls for processing, with {self.config['max_concurrent_thread']} available workers")

            self.clean_up()

        def _start(self, target: Tuple[str, int]):
            """Actually starts scraping

            Arguments:
                target {Tuple[str, int]} --  the url to scrape, it should be contained in a tuple along with the page number (<Actual URL>, <Page represented by URL>)

            Raises:
                SystemExit: exception gets raised if the user requested exit from interpreter manually via Ctrl+C, used to bypass the CatchAll Exception handling
            """
            try:
                url, page_number = target

                time.sleep(self.config["delay_start"])

                # Initializes page specific directory
                page_path = os.path.join(self.master_directory, f"{page_number}")
                self.logger.debug(f"Created page specific directory at: {page_path}")
                os.makedirs(page_path, exist_ok=True)
                self.directory_created.append(page_path)

                self.logger.info(f"Processing page: {page_number}")
                img_data_all = self.process_page(url)  # return large list contains dict of each image and it's info
                for img_data in img_data_all:
                    if (self.are_requirements_satisfied(img_data)):
                        self.write_csv_entry(img_data)

                        if (not self.config["collect_data_only"]):  # If the user want the image too
                            dl_path = page_path
                            if self.config["use_submission_specific_directory"]:
                                dl_path = os.path.join(page_path, img_data["image_id"])
                                os.makedirs(dl_path, True)
                                self.logger.debug(f"Using Submission specific directory at: {dl_path}")
                            for index, img_url in enumerate(img_data["image_links"]):
                                self.logger.debug(f"Downloading image: {img_data['image_id']}")
                                self._download_image(img_url, img_data, dl_path, index)

            except (KeyboardInterrupt):
                self.logger.fatal("Ctrl+C Received. Terminating")
                raise SystemExit(0)
            except ProcessLookupError:
                self.logger.exception("Unexpected exception occurred. Thread Will Exit.")
                return

        def _download_image(self, img_url: str, img_data: dict, path: str, img_index: int):
            """Wrapper for Utils.download_image (self.download_image)

                Automatically constructs the filename, the save path
                Request header (Referrers and User-Agent), and request cookies

            Arguments:
                img_url {str} -- the url for the actual image file to download
                img_data {dict} -- the meta-data of the image, used to construct the downloaded image filename
                path {str(path-like)} -- the path to save the downloaded image to
                img_index {int} -- TODO

            Returns:
                str(path-like) -- the abslute path of downloaded image
            """
            # CONSTRUCTS REQUEST HEADER
            header = self.request_header.copy()
            if self.url_as_referer:
                header.update({"Referer": img_data["image_parent_link"]})

            if "{img_index}" in self.config["filename_string"]:
                file_name = self.config["filename_string"].format(**img_data, img_index=img_index)
            else:
                file_name = self.config["filename_string"].format(**img_data)
            file_path = os.path.join(path, file_name)

            return self.download(img_url, file_path, header, self.request_cookie)

        def write_csv_entry(self, data: dict):
            self.csv_io.write(self.config["csv_entry_string"].format(**data).encode("utf-8"))
            self.csv_io.write("\n".encode("utf-8"))
            if self.config["flush_csv_imminently"]:
                self.csv_io.flush()
                os.fsync(self.csv_io.fileno())

        def initialize_file_and_directory(self):
            """Initializes IO for CSV files and create folders to store scraped data

                Creates Master directory, opens CSV File for writing
            """
            master_directory_name = self.config["master_directory_name_string"].format(**self.config.get_config_dict())
            self.master_directory = os.path.abspath(os.path.join(self.config["save_path"], master_directory_name))
            os.makedirs(self.master_directory, exist_ok=True)
            self.logger.info(f"Created master directory at: {self.master_directory}")

            csv_path = os.path.abspath(os.path.join(self.master_directory, "data.csv"))
            self.csv_io = open(csv_path, "wb")

            self.logger.info(f"Created CSV file for collected image at: {csv_path}")

            # Write the headers of the CSV
            csv_header = self.config["csv_entry_string"].replace("{", "").replace("}", "") + "\n"
            self.logger.debug("Writing CSV header")
            self.csv_io.write(csv_header.encode("utf-8"))

        def clean_up(self):
            self.csv_io.close()

            if self.config["merge_file"]:
                dir_merge = os.path.join(self.master_directory, "merged")
                os.mkdir(dir_merge)
                for directory in self.directory_created:  # merge each directory
                    self.merge_dirs(directory, dir_merge,
                                    keep_separate=self.config["merge_file_keep_separate"],
                                    keep_parent_directory=self.config["use_submission_specific_directory"])

    return ScraperBase(*args, **kwargs)
