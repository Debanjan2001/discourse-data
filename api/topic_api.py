from blog_crawler import blog_crawler
import requests
from bs4 import BeautifulSoup
import math
import json



image_extensions = set(["jpeg","jpg","webp","png","svg","gif","bmp"])

def structure_post(post,site_url,blog_site_slug,first_post = False):

    baseurl = site_url.rsplit("/",2)[0]
    # print(first_post)
    try:
        html_element = post["cooked"]
        soup = BeautifulSoup(html_element, "html.parser")
        links = post.get("link_counts",[])


        connected_links = []
        for link in links:
            try:
                if baseurl in link["url"]:
                    connected_links.append({
                        "title":link.get("title",""),
                        "url":link.get("url","null"),
                        "type":"post",
                        "clicks":link.get("clicks","null"),
                    })
                    
                elif  link["url"].rsplit(".",1)[-1] in image_extensions:
                        connected_links.append({
                            "title":link.get("title",""),
                            "url":link.get("url","null"),
                            "type":"image",
                            "clicks":link.get("clicks","null"),
                        })

                elif blog_site_slug in link["url"]:

                    connected_links.append({
                        "title":link.get("title",""),
                        "url":link.get("url","null"),
                        "type":"blog",
                        "clicks":link.get("clicks","null"),
                        "description": (blog_crawler(url = link.get("url"),blog_site_slug=blog_site_slug) if first_post else "Ignored")
                    })
            except:
                pass

        post_data = {
            "id" : post["id"],
            "post_number":post["post_number"],
            "url": site_url + f"/{post['post_number']}",
            "author" : {    
                "username":post["username"],
                "name":post["name"],
                "user_id":post["user_id"],
                "url": baseurl + f"/u/{post['username']}",
            },
            "links":connected_links,
            "desciription":soup.get_text(),
            "created_timestamp": post["created_at"],
            "score":post["score"],
            "likes": post["actions_summary"][0]["count"] if post["actions_summary"] else 0,
            "reply_count":post["reply_count"],
            "reply_to_post_number":post["reply_to_post_number"],
            "reads":post["reads"],
            "readers_count":post["readers_count"],
        }

        return post_data
    except Exception as e:
        raise(e)


def topic_extractor(url="",max_posts=20,blog_site_slug = ""):

    data = {
        "topic_details":{},
        "posts":[]
    }

    try:
        topic_request = requests.get(url = url)

        site_url = url.rsplit(".",1)[0]

        if topic_request.status_code != 200:
            raise Exception(f"{topic_request.reason}")

    except Exception as e:
        raise(e)

    try:
        topic = topic_request.json()

        topic_details = {
            "id": topic.get("id","null"),
            "categeory_id" : topic.get("category_id","null"),
            "title":topic.get("title",""),
            "url": site_url,
            "slug":topic.get("slug",""),
            "tags":topic.get("tags",[]),
            "posts_count": topic.get("posts_count",0),
            "created_timestamp":topic.get("created_at","null"),
            "views": topic.get("views",0),
            "reply_count": topic.get("reply_count",0),
            "like_count": topic.get("like_count",0),
        }

        print(">>> Started All Posts in Page 1")

        posts_per_page = topic["chunk_size"]
        pages = math.ceil( min(topic_details["posts_count"],max_posts) / posts_per_page )

        for cnt,post in enumerate(topic["post_stream"]["posts"]):
            try:
                post_data = structure_post(post = post, site_url = site_url, blog_site_slug = blog_site_slug,first_post = (cnt == 0))
                data["posts"].append(post_data)
            except Exception as e:
                print(e)
                continue

        print(">>> Finished All Posts in Page 1")


        for page in range(2,pages+1):

            print(f">>> Requested All Posts in Page {page}")

            next_page_url = url + f"?page={page}"
            topic_request = requests.get(url = next_page_url)
            
            if topic_request.status_code != 200:
                print(f"Could not GET Page {page}.\nReason:{topic_request.reason}")
                continue

            topic = topic_request.json()

            for post in topic["post_stream"]["posts"]:
                try:
                    post_data = structure_post(post=post,site_url=site_url,blog_site_slug=blog_site_slug)
                    data["posts"].append(post_data)
                except Exception as e:
                    print(e)
                    continue

            print(f">>> Finished All Posts in Page {page}")
            
        data["topic_details"] = topic_details
        return data

    except Exception as e:
        raise(e)

if __name__ == "__main__":

    url = "https://commons.commondreams.org/t/critics-warn-biden-that-30-methane-reduction-by-2030-not-good-enough/131897.json"
    blog_site_slug = "https://www.commondreams.org"

    file = open("topic-api.json","w")
    try:
        topic_data = topic_extractor(url= url,max_posts=20,blog_site_slug=blog_site_slug)
        file.write(
            json.dumps(topic_data,indent = 4)
        )
        file.close()

    except Exception as e:
        print(e)

    



