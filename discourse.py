import sys
import json
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from discourse_topic_crawler import topic_crawler


configuration = {
    "max_topics": 5,
    "max_posts": 5,
    0: {
        "name": "boingboing",
        "baseurl": "https://bbs.boingboing.net",
        "wishlist": ["boing", "general"],
        "category-header-id": "ember24",
    },
    1: {
        "name": "drownedinsound",
        "baseurl": "https://community.drownedinsound.com",
        "wishlist": [
            "Music","Social"
        ],
        "category-header-id": "ember26",
    },
    2: {
        "name": "commondreams",
        "baseurl": "https://commons.commondreams.org",
        "wishlist": ["News & Views", "FAQ"],
        "category-header-id": "ember25",
    },
}


def discourse_crawler(
    baseurl: str = "",
    driver: WebDriver = None,
    header_id: str = "",
    mywish: list = [],
    max_topics=3,
    max_posts=3,
):

    """
    @params =>
        # baseurl = URL of site
        # driver = instance of webdriver ( I am using Chrome 92)
        # header_id = id of commmon discourse header id
        # mywish = list of categories in my wishlist

    @returns =>
        # data : list of extracted data
    """

    data = []

    try:
        # Go to site
        driver.get(baseurl)

        # Category Dropdown
        dropdown = driver.find_element_by_id(f"{header_id}-header")
        dropdown.click()

        for list_item in driver.find_element_by_id(
            f"{header_id}-body"
        ).find_elements_by_tag_name("li"):
            category_name = list_item.find_element_by_class_name("category-name").text

            if category_name not in mywish:
                continue

            print(f"STARTED --- CATEGORY: {category_name}")

            num_topics = list_item.find_element_by_class_name("topic-count").text[2:]
            try:
                category_description = list_item.find_element_by_class_name(
                    "category-desc"
                ).text
            except:
                category_description = ""

            """
                Work by opening a new Tab
                Otherwise it wont work due to Stale Element Exception
                BBS has an advantage . just append the category name to baseurl and it will redirect
            """

            # Load the page
            next_pageurl = baseurl + f"/c/{category_name}"

            driver.execute_script("window.open('');")

            # Switch to the new window and open new URL
            driver.switch_to.window(driver.window_handles[1])

            driver.get(next_pageurl)

            category_data = {
                "category_name": category_name,
                "category_description": category_description,
                "category_link": driver.current_url,
                "num_topics": num_topics,
            }

            """
            Be careful the element class names might change sometimes.
            """
            topics = driver.find_elements_by_class_name("raw-topic-link")[:max_topics]
            
            # print(len(topics))

            topics_data = []
            # print(topics)

            for cnt, topic in enumerate(topics, 1):

                topic_url = topic.get_attribute("href")
                # print(topic_url)

                driver.execute_script("window.open('');")
                # Switch to the new window and open new URL
                driver.switch_to.window(driver.window_handles[2])

                try:
                    topic_data = topic_crawler(
                        url=topic_url, driver=driver, max_posts=max_posts
                    )
                    topics_data.append(topic_data)
                except Exception as e:
                    print(e)
                    pass

                # Closing new_url tab
                driver.close()

                # Switching to old tab
                driver.switch_to.window(driver.window_handles[1])

            data.append({"category": category_data, "topics": topics_data})

            driver.close()

            # Switching to old tab
            driver.switch_to.window(driver.window_handles[0])

            print(f"FINISHED --- CATEGORY: {category_name}")

    except Exception as e:
        print(e)

    return data


if __name__ == "__main__":

    debug = True
    myKey = 2

    if len(sys.argv)>1:
        myKey = int(sys.argv[1])

    if debug:
        driver = webdriver.Chrome()
        driver.maximize_window()
    else:
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)

    baseurl = configuration[myKey]["baseurl"]
    mywish = configuration[myKey]["wishlist"]
    max_topics = configuration["max_topics"]
    max_posts = configuration["max_posts"]
    header_id = configuration[myKey]["category-header-id"]
    filename = configuration[myKey]["name"]

    print(baseurl)

    data = discourse_crawler(
        baseurl=baseurl,
        driver=driver,
        header_id=header_id,
        mywish=mywish,
        max_topics=max_topics,
        max_posts=max_posts,
    )

    # Save data
    with open(f"{filename}.json", "w") as file:
        json_obj = json.dumps(data, indent=4)
        file.write(json_obj)

    # Close the driver
    driver.close()
