from enum import Enum
import os

DATA_DIRECTORY = 'tmp/data'
JSON_DATA_DIRECTORY = os.path.join(DATA_DIRECTORY,"json_data")
RAW_REQUESTS_DIRECTORY = os.path.join(DATA_DIRECTORY,"raw_requests")

os.makedirs(DATA_DIRECTORY,exist_ok=True)
os.makedirs(JSON_DATA_DIRECTORY,exist_ok=True)
os.makedirs(RAW_REQUESTS_DIRECTORY,exist_ok=True)

class CrawlerBaseURLs(Enum):
    BASE_URL = "https://www.amazon.com/s"

class CrawlerConstants(Enum):
    COOKIES = {
        'session-id': '145-4902261-2194662',
        'session-id-time': '2082787201l',
        'i18n-prefs': 'USD',
        'sp-cdn': '"L5Z9:PK"',
        'ubid-main': '131-4180572-4581705',
        'skin': 'noskin',
        'session-token': 'YduDFQ3owlMdCDWeH06gDUxiLjCGx9M8GZi7YTJTZ95GWiok9WKh9nuRXa2SuQdEGpX26sv+tvsqeOwC6qVsLYkWPVzZvMRkJHumKW9Ri7vOkUA74Q1dd6Ey0v9GKVh9lHFxBdHglqQycvhtpKzwAId36Pb1cZgi2646DFyEGFP5FLqWt0c7oMNmeTexjSBtqIOMD9595juUXqQnAfYiOvraLoHfopTdUCn2Ww/qVrC+a6RqEik9hT0a6iUyPR2sSm5FkuPODArY18icAD0OBwlKHUA4CFXI/vVlNuaCpc4gAlsrg50hWDoIlSIJhRmsSGyo/U+3EuWZQGPIlfmdM4geUB3xVFEC',
        'csm-hit': 'tb:21TV4B7HXY93PT4B8PMA+s-21TV4B7HXY93PT4B8PMA|1747309510360&t:1747309510360&adb:adblk_no',
        'rxc': 'ANqE/8cG6wsHoVa3OGk',
    }

    HEADERS = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'device-memory': '8',
        'downlink': '1.35',
        'dpr': '1',
        'ect': '3g',
        'priority': 'u=0, i',
        'referer': 'https://www.amazon.com/',
        'rtt': '250',
        'sec-ch-device-memory': '8',
        'sec-ch-dpr': '1',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-ch-ua-platform-version': '"6.11.0"',
        'sec-ch-viewport-width': '864',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'viewport-width': '864',
    }

    PARAMS = {
        '_encoding': 'UTF8',
        'k': 'gaming headsets',
        'ref': 'nb_sb_noss_2',
        'pd_rd_w': 'VnEwS',
        'content-id': 'amzn1.sym.12129333-2117-4490-9c17-6d31baf0582a',
        'pf_rd_p': '12129333-2117-4490-9c17-6d31baf0582a',
        'pf_rd_r': '21TV4B7HXY93PT4B8PMA',
        'pd_rd_wg': 'dyllh',
        'pd_rd_r': 'b276d8a2-b79c-4ef3-b1b2-a737cc9d573c',
        'ref_': 'pd_hp_d_atf_unk',
    }

class SelectorsConstants(Enum):
    PRODUCT_URL_XPATHS = "//div[contains(@role,'listitem')]/div/div//a[contains(@class,'a-link-normal s-line-clamp-2')]/@href"
    PRODUCT_TITLE_XPATH = '//h1[@id="title"]/span/text()'
    PRODUCT_PRICE_XPATH = '//div[contains(@class,"a-box")]//span[contains(@class,"a-price")]/span[contains(@class,"a-offscreen")]/text()'
    PRODUCT_COLOR_AND_EDITION_XPATH = '//span[@class="selection"]//text()'
    PRICE_Second_Xpath = '//div[contains(@class,"a-box")]//div[contains(@class,"a-column")]//span[contains(@class,"a-size-base")]/text()'
    NEXT_PAGE_XPATH = '//a[contains(@aria-label,"Go to next page")]/@href'
    XPATH_FOR_RATINGS = '//a[contains(@id,"acrCustomerReviewLink")]/span[contains(@id,"acrCustomerReviewText")]/text()'
    XPATH_FOR_FEATURES = '//tr[contains(@class,"a-spacing-small")]//span[contains(@class,"po-break-word")]/text()'
    
class AirTableConstants(Enum):
    TABLE_NAME = "Amazon products"