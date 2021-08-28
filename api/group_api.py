import requests
import os
import json
import math

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

filepath = configuration["directory_name"] + "/" + "groups.json" 
os.makedirs(os.path.dirname(filepath), exist_ok=True)
file = open(filepath,"w")

data = []

try:
    url = configuration["baseurl"] + "/groups.json"

    group_request = requests.get(url).json()

    total_groups = group_request["total_rows_groups"]

    count = 0
    page = 0
    while(count<total_groups):
        print(f">>> Requesting Groups in page{page}")

        baseurl = url
        if page>0:
            baseurl += f"?page={page}"
        group_request = requests.get(baseurl).json()

        count += len(group_request["groups"])

        for group in group_request["groups"]:
            print(f":::: Started Group : {group['name']}")

            try:
                group_data = {
                    "id":group["id"],
                    "url":configuration["baseurl"]+f"/g/{group['id']}",
                    "name":group["name"],
                    "user_count":group["user_count"],
                    "full_name":group["full_name"],
                    "title":group["title"]
                }


                members_url = configuration["baseurl"] + f"/g/{group['name']}/members.json"
                members_request = requests.get(members_url).json()

                users_data = {
                    "members": members_request.get("members",[]),
                    "owners":members_request.get("owners",[])
                }

                data.append({
                    "group_details":group_data,
                    "users":users_data
                })

                print(f":::: Finished Group : {group['name']}\n")

            except Exception as e:
                print(e)
                pass

        print(f">>> Finished Groups in page{page}\n")
        page += 1;

        

except Exception as e:
    print(e)

file.write(json.dumps(data,indent = 4))
file.close()
