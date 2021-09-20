import requests
import os
from bs4 import BeautifulSoup
import json

# configuration = {
#     "directory_name" : "boingboing",
#     "baseurl" : "https://bbs.boingboing.net",
# }


configuration = {
    "directory_name" : "drownedinsound",
    "baseurl" : "https://community.drownedinsound.com",
}


# configuration = {
#     "directory_name" : "commondreams",
#     "baseurl" : "https://commons.commondreams.org",
# }



def all_category_extractor(url, filename, path):

    data = []

    try:
        categories = requests.get(url = url)

        print("Requested Categories")

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

            category_data = {
                "id":category["id"],
                "url": configuration["baseurl"] + f"/c/{category['id']}",
                "name":category["name"],
                "slug":category["slug"],
                "topic_count":category["topic_count"],
                "post_count":category["post_count"],
                "description": category["description_text"],
            }

            data.append(category_data)

        print("Finished Categories")
        return data

    except Exception as e:
        print(e)   
        return data

if __name__ == "__main__":

    filename = "categories.json"
    path = configuration["directory_name"]
    categories_url = configuration["baseurl"] + "/categories.json"
    try:
        categories_data = all_category_extractor(url = categories_url,filename=filename,path = path)

        filepath = path + "/" + filename 
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file = open(filepath,"w")

        print(filepath)

        file.write(json.dumps(categories_data,indent=4))

        file.close()
        
    except Exception as e:
        print(e)




    