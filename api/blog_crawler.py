from bs4 import BeautifulSoup
import requests

sites = [
    "https://boingboing.net",
    "https://www.commondreams.org",
    "https://drownedinsound.com",
]

def blog_crawler(url, blog_site_slug):
    description = ""
    try:
        resp = requests.get(url)
        html = resp.text
        soup = BeautifulSoup(html, 'html.parser')
        text = None
        if blog_site_slug == sites[0]:
            text = soup.find("section")
            for paragraph in text.find_all("p"):
                description += paragraph.get_text()
                description += "\n"

        elif blog_site_slug == sites[1]:
            text = soup.find_all(class_ = "row")[3]
            blocks = text.find_all(class_ = "block")[1:]
            for block in blocks:
                for paragraph in block.find_all("p"):
                    description += paragraph.get_text()
                    description += "\n"
        
        elif blog_site_slug == sites[2]:
            pass
        
    except Exception as e:
        print(e)

    return description 