import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib.request
import logging
import json
from selenium_stealth import stealth

logger = logging.getLogger('selenium')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('selenium.log')
fh.setLevel(logging.INFO)
logger.addHandler(fh)
import chromedriver_binary  # Adds chromedriver binary to path


def create_driver():
    """
    Create selenium driver
    """
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--no-sandbox")
    options.add_argument('--headless')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-dev-shm-usage")  # overcome limited  resource   problems
    options.add_argument(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    return driver


def create_chapter_item(name, url):
    """
    Create chapter_item
    """
    result = {
        "name": name,
        "href": url,
        "image_urls": []
    }

    return result


def open_selenium(url):
    """
    Return chapter data list

    input:
    url: url of the manga ("https://www.nettruyenup.com/truyen-tranh/imawa-no-kuni-no-alice")

    result = [{
        "name": name,
        "href": url,
        "image_urls": ["https://u.ntcdntempv3.com/cont...."]
    }]
    """
    driver = create_driver()
    chapter_data_list = []
    try:
        driver.get(url)
        # Check for cloudflare challenge
        challenge = driver.find_elements(by=By.ID, value="challenge-running")
        if challenge:
            logger.info("Cloudflare challenge detected waiting for 10s")
            time.sleep(10)
        # Printing the whole body text
        logger.info("Find list chapter element")
        list_chapters = driver.find_elements(by=By.CLASS_NAME, value="list-chapter")
        if list_chapters:
            logger.info("Found list chapter element, Finding the nav elenemt")
            list_element = list_chapters[0]
            navs = list_element.find_elements(by=By.TAG_NAME, value='nav')
            if navs:
                logger.info("Found nav element. Loading chapter urls...")
                nav = navs[0]
                rows = nav.find_elements(by=By.CLASS_NAME, value="row")
                if rows:
                    logger.info("Number of chapter: {}".format(len(rows)))
                    logger.info("Loading chapter urls...")
                    for row in rows:
                        row_classes = row.get_attribute("class")
                        if "less" in row_classes:
                            driver.execute_script("arguments[0].setAttribute('class', 'row')", row)
                        chapter_divs = row.find_elements(by=By.CLASS_NAME, value="chapter")
                        if chapter_divs:
                            chapter_link_elements = chapter_divs[0].find_elements(by=By.TAG_NAME, value="a")
                            if chapter_link_elements:
                                chapter_link_element = chapter_link_elements[0]
                                href = chapter_link_element.get_attribute("href")
                                chapter_name = chapter_link_element.text
                                # logger.info("{}: {}".format(chapter_link_element.text, href))
                                logger.info("{}: {}".format(chapter_name, href))
                                chapter_data_list.append(create_chapter_item(chapter_name, href))

                else:
                    logger.error("Not found any chapter")
        else:
            logger.error("Not found list chapter")

        if not chapter_data_list:
            logger.info("Stop loading due to no chapter found")
            with open("nettruyen.html", mode="w") as file:
                file.write(driver.page_source)
                file.close()
            driver.quit()
            return chapter_data_list

        # Reverse the list, first chapter is in the end
        for chapter_item in reversed(chapter_data_list):
            logger.info("Loading {}".format(chapter_item.get("name")))
            href = chapter_item.get("href") or ''
            if not href:
                logger.warning("--{} not loaded due to invalid href: {}".format(chapter_item.get("name"),
                                                                                chapter_item.get("href")))
                continue

            driver.get(href)
            # get all element container images
            page_chapters = driver.find_elements(by=By.CLASS_NAME, value="page-chapter")
            if page_chapters:
                for page_chapter in page_chapters:
                    imgs = page_chapter.find_elements(by=By.TAG_NAME, value="img")
                    if imgs:
                        image_url = imgs[0].get_attribute("src") or ''
                        chapter_item.get('image_urls').append(image_url)
            logger.info("number of images: {}".format(chapter_item.get('image_urls')))
    except Exception as e:
        logger.error("Error: ")
        logger.error(e)

    # with open("chapters.txt", mode="w") as file:
    #     for chapter in chapter_data_list:
    #         file.writelines("*******************************\n")
    #         file.writelines(json.dumps(chapter))
    #     file.close()

    driver.quit()
    # img = driver.find_element(by=By.XPATH, value='//*[@id="page_2"]/img')
    # src = img.get_attribute('src')
    # opener = urllib.request.build_opener()
    # opener.addheaders = [('Referer', 'https://www.nettruyenup.com/truyen-tranh/imawa-no-kuni-no-alice')]
    # urllib.request.install_opener(opener)
    # urllib.request.urlretrieve(src, "local-filename.jpg")
    return chapter_data_list
