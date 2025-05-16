from product_crawler import main as main_crawler
from loguru import logger

def main():
    logger.info("Starting The Main Crawler for Amazon Products Crawler")
    main_crawler()

if __name__ == '__main__':
    main()