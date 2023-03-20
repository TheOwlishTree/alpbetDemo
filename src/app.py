import requests
import os
from bs4 import BeautifulSoup
import logging
import re


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebCrawler:
    def __init__(self, max_ext, max_depth, unique=True):
        self.url_unique_helper = []
        self.max_ext: int = max_ext
        self.max_depth: int = max_depth
        self.unique: bool = unique
        self.current_depth = 0

        logger.info(f"Config: max_ext: {max_ext}, max_depth: {max_depth}, unique: {unique}")

    def get_soup(self, url):
        f = requests.get(url)
        return BeautifulSoup(f.content, 'html.parser')

    def write_html_to_file(self, depth, name, content):
        """ Parse file name, Create folder, And write to file """
        # remove https
        name = name.removeprefix("https://")
        # To be safe
        name = name.removeprefix("http://")
        # remove trailing slash if exists
        name = name.removesuffix("/")

        # Really not feeling very confident about this one. I hate regex
        name = re.sub(r"[^\w\d]+", "_", name)

        # Filename is the depth as folder name, and the filename with .html
        filename = f"results/{depth}/{name}.html"

        logger.info(f"Will write into {filename}")
        # Make dir if none exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Write to file
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)

    def get_href_from_soup(self, soup):
        """ Get number of max_ext of href from soup. That sounds confusing. """
        ret = []
        for anchor in soup.findAll("a", href=True):
            href = anchor.get("href")
            if self.unique:
                if href not in self.url_unique_helper:
                    self.url_unique_helper.append(href)
                    ret.append(href)
            else:
                self.url_unique_helper.append(href)
                ret.append(href)
            if len(ret) == self.max_ext:
                break
        return ret

    def run(self, url, depth=0):
        try:
            if depth <= self.max_depth:

                soup = self.get_soup(url)
                self.url_unique_helper.append(url)
                self.write_html_to_file(depth=depth, name=url, content=str(soup))

                hrefs = self.get_href_from_soup(soup)
                for href in hrefs:
                    self.run(href, depth+1)
        except requests.exceptions.MissingSchema:
            # For some reason, there are use cases when it has like //ynet.com instead of https://ynet, making it
            # go crazy, just ignore and move to the next one
            pass
        except requests.exceptions.InvalidSchema:
            # For another reason I don't really get, it sometime tries to do request to javascript void, something with
            # how ynet writes their href. Ignore and move on
            pass
        except requests.exceptions.ConnectionError as e:
            # This one might actually be relevant, so atleast log it. Sites like Yad2 gets max retries. Might be my
            # connection, or it might be some defense from ddos on their parts, or maybe just cors. Anyways, move on,
            # but do log.
            logger.warning(f"An error occured with the url {url}. Please make sure nothing broke", e)
            pass
        except Exception as e:
            logger.critical(f"Somethine VERY wrong which i did not predict happened while running on {url}. "
                            f"Please freak out", e)
            raise
