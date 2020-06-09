from urllib import parse

import os
import shutil
import requests

class Utils:


    def __init__(self, logger):
        self.logger = logger
        super().__init__()


    def download(self, target_url: str, download_dst: str, header: dict, cookie: dict) -> str:
        """download file from target url

        Arguments:
            target_url {str} -- the url of the file that's needed to be downloaded
            download_dst {str} -- the path of the file the download data will be saved to
            header {dict} -- the header that will be used to download the file
            cookie {dict} -- the cookie will be used to download the file

        Returns:
            str -- the path of the downloaded file
        """
        target_url = parse.unquote(target_url)
        dst = os.path.abspath(download_dst)
        self.logger.info("Downloading: {}".format(target_url))
        r = requests.get(target_url, headers=header, cookies=cookie)

        if r.status_code >= 400:
            self.logger.error("Failed to download: {} | Server responded with code: {}".format(target_url, r.status_code))
            return;

        with open(dst, "wb") as f:
            f.write(r.content)

        self.logger.debug("Downloaded: {}".format(target_url))

        return dst


    def merge_dirs(self, src, dst, keep_separate=True, keep_parent_directory=False):
        """
        Put all files from multiple dir into one
        """
        os.makedirs(dst, exist_ok=True)
        self.logger.info("Trying to merge all files in {} -> {}".format(src, dst))

        for (directory, dirnames, filenames) in os.walk(src):
            for f in dirnames if keep_parent_directory else filenames:
                file_abs_path = os.path.abspath(os.path.join(directory, f))
                if os.name == "nt":  # work around for windows 256 character path limit
                    file_abs_path = ("\\\\?\\" + file_abs_path)

                try:
                    if keep_separate:
                        # Copy Require full path name, including the filename
                        full_dst = os.path.join(dst, file_abs_path.split(os.sep)[-1]) # get the source filename and add it to dst path
                        self.logger.debug("Copying file: {} -> {}".format(file_abs_path, full_dst))
                        if keep_parent_directory:
                            shutil.copytree(file_abs_path, full_dst)
                        else:
                            shutil.copy(file_abs_path, full_dst)
                    else:
                        self.logger.debug("Moving file: {} -> {}".format(file_abs_path, dst))
                        shutil.move(file_abs_path, dst)
                except Exception:
                    self.logger.exception("Failed to move/copy file: {} -> {}".format(file_abs_path, dst))
                    continue
        if not keep_separate:
            shutil.rmtree(src)
