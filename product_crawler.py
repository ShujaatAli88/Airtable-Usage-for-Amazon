import requests
import json
from uuid import uuid4
import os
from lxml import etree
from loguru import logger
from models import ModelData
from constants import (
    RAW_REQUESTS_DIRECTORY,
    JSON_DATA_DIRECTORY,
    CrawlerBaseURLs,
    CrawlerConstants,
    SelectorsConstants,
)
from airtable_manager import AirTableManager
# from utils import snake_to_title

airtable_obj = AirTableManager()


class AmazonCrawler:
    def __init__(self):
        self.all_products_urls = []

    def initial_request(self):
        """make the request to product base URL."""
        response = requests.get(
            CrawlerBaseURLs.BASE_URL.value,
            params=CrawlerConstants.PARAMS.value,
            cookies=CrawlerConstants.COOKIES.value,
            headers=CrawlerConstants.HEADERS.value
        )

        if response.status_code == 200:
            with open("initial.html","w") as f:
                f.write(response.text)
            logger.info("Request Successfull.")
            return response
        else:
            logger.error(f"Request Not Successfull:{response.status_code}")
            return None
        
    def get_products_urls(self, initial_response):
        """Get URLs of all the products from all pages."""
        tree = etree.HTML(initial_response.text)
        product_urls = tree.xpath(SelectorsConstants.PRODUCT_URL_XPATHS.value)
        self.all_products_urls.extend(product_urls)
        print(self.all_products_urls)

        next_page = tree.xpath(SelectorsConstants.NEXT_PAGE_XPATH.value)
        while next_page:
            logger.info("Next Page Found. Calling it.")
            next_page_href = next_page[0].strip()
            next_page_url = f"https://www.amazon.com{next_page_href}"
            page_no = next_page_url.split("&")[1].split("=")[1]

            response = requests.get(
                next_page_url,
                cookies=CrawlerConstants.COOKIES.value,
                headers=CrawlerConstants.HEADERS.value
            )
            if response.status_code == 200:
                with open("second.html", "w") as f:
                    f.write(response.text)

                tree = etree.HTML(response.text)
                product_urls = tree.xpath(SelectorsConstants.PRODUCT_URL_XPATHS.value)
                self.all_products_urls.extend(product_urls)

                # next_page = tree.xpath(SelectorsConstants.NEXT_PAGE_XPATH.value)
                next_page = False
                logger.info(f"Request Successful for Page Number: {page_no}")
            else:
                logger.warning(f"Request Was Not Successful: {response.status_code}")
                break


    def get_product_responses(self, *, product_urls: list):
        """make requests to product detail page."""
        raw_responses = []
        for url in product_urls:
            if "https://" not in url:
                product_url = f"https://www.amazon.com/{url}"
                print(f"PRODUCT URLLLLLLLLLLL:::::::::::::{product_url}")
            else:
                product_url = url

            response = requests.get(
                product_url,
                cookies=CrawlerConstants.COOKIES.value,
                headers=CrawlerConstants.HEADERS.value
            )
            if response.status_code == 200:
                logger.info(f"Raw Response Fetched Successfully for : {product_url}")
                raw_responses.append(response)
            else:
                logger.error(f"Request to This Url was not Successfull : {product_url}")
                continue
            # break

        return raw_responses

    # Ensure this function converts keys correctly from snake_case to Title Case
    def snake_to_title(self, snake_str):
        return snake_str.replace("_", " ")

    def parse_product_response(self, *, response: list, product_urls: list):
        all_records = []
        for res, url in zip(response, product_urls):
            tree = etree.HTML(res.text)
            ratings = tree.xpath(SelectorsConstants.XPATH_FOR_RATINGS.value)
            features = tree.xpath(SelectorsConstants.XPATH_FOR_FEATURES.value)

            # Extract title
            title_elements = tree.xpath(SelectorsConstants.PRODUCT_TITLE_XPATH.value)
            title = title_elements[0].strip() if title_elements else "Unknown Title"
            if not title_elements:
                logger.warning(f"Title is missing or couldn't be extracted for: {url}")

            # Extract product price
            product_price_elements = tree.xpath(
                SelectorsConstants.PRODUCT_PRICE_XPATH.value
            )
            if not product_price_elements:
                product_price_elements = tree.xpath(
                    SelectorsConstants.PRICE_Second_Xpath.value
                )

            product_price = (
                product_price_elements[0].strip() if product_price_elements else "Null"
            )
            if not product_price_elements:
                logger.warning(f"Price is missing or couldn't be extracted for: {url}")

            # Store product details
            product_details = {
                "product_id": str(uuid4()),
                "product_title": title,
                "product_price": product_price,
                "product_url": res.url,
                "product_rating": ratings[0]
                if len(ratings) > 1
                else "No Rating Given So Far",
                "brand": features[0].strip()
                if len(features) > 0
                else "Brand Name not Given",
                "color": features[1].strip()
                if len(features) > 1
                else "Color Not Given",
                "form_factor": features[2].strip()
                if len(features) > 2
                else "Form Control Not Provided",
                "noise_control": features[3].strip()
                if len(features) > 3
                else "Noise Control Not Available",
                "headphone_jack": features[4].strip()
                if len(features) > 4
                else "Headphones Jack Not Available",
            }

            # Save response
            self.save_response(product_details, res, product_price)
            model_item = self.parse_response(product_details)
            model_dict = model_item.model_dump()

            # Transform keys using snake_to_title
            data_dict = {
                self.snake_to_title(key): value for key, value in model_dict.items()
            }

            logger.info("Calling The Upsert Method...")
            all_records.append(data_dict)
            logger.debug(
                f"Transformed data_dict: {data_dict}"
            )  # Log transformed dictionary
            airtable_obj.upsert_data(data=data_dict)
            logger.info(f"Records Upserted So far:{len(all_records)}")

    def save_response(self, product_details, response, price):
        raw_data_path = os.path.join(RAW_REQUESTS_DIRECTORY, f"{price}.html")
        with open(raw_data_path, "w", encoding="utf-8") as file:
            file.write(response.text)

        json_data_path = os.path.join(JSON_DATA_DIRECTORY, f"{price}.json")
        with open(json_data_path, "w", encoding="utf-8") as file:
            file.write(str(product_details))

    def parse_response(self, data: dict) -> ModelData:
        """Here we validate the data using The pydantic models."""
        logger.info("Validating The Data")
        item = ModelData(
            product_id=data["product_id"],
            product_title=data["product_title"],
            product_price=data["product_price"],
            product_url=data["product_url"],
            product_rating=data["product_rating"],
            brand=data["brand"],
            color=data["color"],
            form_factor=data["form_factor"],
            headphone_jack=data["headphone_jack"],
            noise_control=data["noise_control"],
        )
        return item


def main():
    amazon_manager = AmazonCrawler()
    initial_response = amazon_manager.initial_request()
    if initial_response is None:
        logger.error(
            "initial Response is None Check The Request Again Tom get response"
        )

    amazon_manager.get_products_urls(initial_response)
    responses = amazon_manager.get_product_responses(
        product_urls=amazon_manager.all_products_urls
    )
    amazon_manager.parse_product_response(
        response=responses, product_urls=amazon_manager.all_products_urls
    )
