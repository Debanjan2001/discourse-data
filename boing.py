import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

debug = False

if debug:
    driver = webdriver.Chrome()
    driver.maximize_window()
else:
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)


data = []

baseurl = "https://bbs.boingboing.net"
max_topics = 5
max_posts = 5
mywish = ["general", "boing"]

from boing_topic_crawler import topic_crawler

try:
    # Go to site
    driver.get(baseurl)

    # Category Dropdown
    dropdown = driver.find_element_by_id("ember24-header")
    dropdown.click()

    for list_item in driver.find_element_by_id(
        "ember24-body"
    ).find_elements_by_tag_name("li"):
        category_name = list_item.find_element_by_class_name("category-name").text

        if category_name not in mywish:
            continue

        print(f"STARTED --- CATEGORY: {category_name}")

        num_topics = list_item.find_element_by_class_name("topic-count").text[2:]
        category_description = list_item.find_element_by_class_name(
            "category-desc"
        ).text

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

        topics = driver.find_elements_by_class_name("raw-topic-link")[:max_topics]
        # print(len(topics))

        topics_data = []

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
    print(str(e))

time.sleep(2)
driver.close()

# Save data
with open(f"data.json", "w") as file:
    json_obj = json.dumps(data, indent=4)
    file.write(json_obj)
