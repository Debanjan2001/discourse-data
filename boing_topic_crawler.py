import json
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options


def topic_crawler(url: str = None, driver: WebDriver = None, max_posts = 5):

    try:
        driver.get(url)

        try:
            driver.find_element_by_class_name(
                "widget-button.btn.btn.no-text.btn-icon"
            ).click()
        except:
            pass

        topic_name = driver.find_element_by_tag_name("h1").text
        topic_info = driver.find_element_by_class_name("topic-map")
        metrics = topic_info.find_elements_by_tag_name("span")
        
       

        try:
            popular_links_attached = topic_info.find_element_by_class_name("topic-links")
            popular_links_attached_urls = [
            link.get_attribute("href") for link in
                popular_links_attached.find_elements_by_tag_name("a")
            ]
        except Exception as e:
            popular_links_attached_urls = []
            
        print(f"STARTED --- TOPIC: {topic_name}")

        topic_data = {
            "topic_title": topic_name,
            "topic_id": url.split("/")[-1],
            "topic_url": url,
            "created_timestamp": metrics[0].get_attribute("title"),
            "replies": metrics[2].text,
            "views": metrics[3].text,
            "users": metrics[4].text,
            "likes": metrics[5].text,
        }

        try:
            topic_data["total_links_attached"] =  metrics[6].text,
        except:
            topic_data["total_links_attached"] = "0"

        try:
            topic_data["popular_links"] = popular_links_attached_urls
        except:
            topic_data["popular_links"] = []

        """
            Crawl Top 5 posts in this topic
        """
        posts = driver.find_elements_by_class_name("topic-post")[:max_posts]

        posts_data = []
        for post_id, post in enumerate(posts, 1):
            
            print(f"STARTED --- POST: {post_id}")

            post_author = post.find_element_by_class_name("first.username").text
            post_link = url + f"/{post_id}"
            try:
                post_replies = post.find_element_by_class_name("show-replies").text
            except:
                post_replies = "0 Reply"
           
            try:
                post_likes = post.find_element_by_class_name("like-count").text
            except:
                post_likes = "NULL"
            post_description = post.find_element_by_class_name("cooked").text

            try:
                linked_posts = post.find_element_by_class_name("post-links-container")
                linked_post_urls = [
                    link.get_attribute("href") for link in 
                    linked_posts.find_elements_by_tag_name("a")
                ]
            except Exception as e:
                linked_post_urls = []

            current_data = {
                "post_id": post_id,
                "post_link": post_link,
                "post_author": post_author,
                "post_description": post_description,
                "post_replies": post_replies,
                "post_likes": post_likes,
                "linked_posts":linked_post_urls,
            }

            posts_data.append(current_data)
            
            print(f"FINISHED --- POST: {post_id}")

        topic_data["topic_author"] = posts_data[0]["post_author"]

        data = {
            "topic_details": topic_data,
            "posts": posts_data,
        }   

        print(f"FINISHED --- TOPIC: {topic_name}")

        return data

    except Exception as e:
        print(e)


if __name__ == "__main__":

    baseurl = "https://bbs.boingboing.net/t/good-encouraging-stuff/158198"

    debug = False

    if debug:
        driver = webdriver.Chrome()
        driver.maximize_window()
    else:
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)

    data = topic_crawler(baseurl, driver)

    with open("topic.json", "w") as file:
        json_obj = json.dumps(data, indent=4)
        file.write(json_obj)

    driver.close()
