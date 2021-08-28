import requests
import os
from bs4 import BeautifulSoup
import json
import math
from topic_api import topic_extractor

# configuration = {
#     "directory_name" : "boingboing",
#     "baseurl" : "https://bbs.boingboing.net",
#     "mywish" : ["boing","general"],
#     "slug": "boingboing.net",
# }

# configuration = {
#     "directory_name" : "drownedinsound",
#     "baseurl" : "https://community.drownedinsound.com",
#     "mywish" : ["Music","How to Dis"],
#     "slug": "drownedinsound.com",
# }

configuration = {
    "directory_name" : "commondreams",
    "baseurl" : "https://commons.commondreams.org",
    "mywish" : ["FAQ","News & Views"],
    "slug": "commondreams.org",
}

print(":::::::::::::::::::::::::::")
print(configuration["baseurl"])
print(":::::::::::::::::::::::::::\n")


max_topics = 30
max_posts = 4000

filepath = configuration["directory_name"] + "/" + "data.json" 
os.makedirs(os.path.dirname(filepath), exist_ok=True)
file = open(filepath,"w")

url = configuration["baseurl"] + "/categories.json"

master_data = []

try:
    categories = requests.get(url = url)

    if categories.status_code == 200:
        pass
    else:
        print(categories.status_code)
        print(categories.reason)

except Exception as e:
    print(e)
    exit()

try:
    all_categories = categories.json().get("category_list").get("categories",[])

    for category in all_categories:

        single_category_data = {}
        if category["name"] not in configuration["mywish"]:
            continue
        
        try:
            category_data = {
                "id":category["id"],
                "url": configuration["baseurl"] + f"/c/{category['id']}",
                "name":category["name"],
                "slug":category["slug"],
                "topic_count":category["topic_count"],
                "post_count":category["post_count"],
                "description": category.get("description_text",""),
            }

            try:
                print(f"*** Requesting Category : {category_data['name']} ***")

                category_url = configuration["baseurl"] + f"/c/{category_data['id']}.json"
                category_request_json = requests.get(category_url).json()
                
                topics_per_page = category_request_json["topic_list"]["per_page"]

                pages = math.ceil(min(category_data["topic_count"],max_topics) / topics_per_page)

                topics_data = []

                for page in range(1,pages+1):
                    try:
                        print(f"### Requesting Topics from Page {page} :: Category : {category_data['name']} ###")
                        page_url = category_url + f"?page={page}"
                        topic_list = requests.get(page_url).json()["topic_list"]["topics"]

                        for topic in topic_list:
                            topic_url = configuration["baseurl"] + f"/t/{topic['id']}.json"
                            print(f"::> Starting Topic :{topic['title'][:50]}...")
                            try:
                                single_topic = topic_extractor(url = topic_url,max_posts=max_posts,site_slug=configuration["slug"])
                                topics_data.append(
                                    single_topic
                                )  

                                print(f"::> Finished Topic :{topic['title'][:50]}...\n")

                            except Exception as e:
                                print(e)
                                continue

                        print(f"### Finished Topics from Page {page} :: Category : {category_data['name']} ###\n")
                    except Exception as e:
                        print(e)
                        continue


                print(f"*** Finished Category : {category_data['name']} ***\n")

            except Exception as e:
                print(e)
                print("Could not extract this category")

            single_category_data["category_details"] = category_data
            single_category_data["topic_list"] = topics_data

            master_data.append(single_category_data)

        except Exception as e:
            print(e)
            pass 

except Exception as e:
    print(e)   

file.write(json.dumps(master_data,indent=4))

file.close()
        



    