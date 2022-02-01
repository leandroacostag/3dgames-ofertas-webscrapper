import requests
from bs4 import BeautifulSoup
import json
import time
import ast

#CONFIG
SLEEP_TIME = 2 #time in seconds to avoid timeout error using telegram api
TOKEN = "bot:token" #telegram token
CHAT_ID = "-number" #channel id
JSONBLOD_ID = "number" #id for your json file to get last postId crawled

request_url = "https://api.telegram.org/bot" + TOKEN

print("Initializaing 3dgames webscrapper execution")

#reading postId from the last execution
lastIdCrawled = requests.get("https://jsonblob.com/api/jsonBlob/" + JSONBLOD_ID)
lastIdCrawled = ast.literal_eval(lastIdCrawled.text)["id"]

#reading last thread number from post landing page
print("Finding last thread crawled...")

URL = "https://foros.3dgames.com.ar/threads/942062-ofertas-online-argentina"
landingPage = BeautifulSoup(requests.get(URL).content, "html.parser")
lastThreadPageNumber = landingPage.find("span", class_="first_last").find("a")["href"][44:49]

#crawling all thread pages until lastIdCrawled is found

crawledPosts = {}
postIds = []

pageNumberToCrawl = lastThreadPageNumber

while lastIdCrawled not in postIds:
    print("Crawling thread number:" + str(pageNumberToCrawl))
    page = BeautifulSoup(requests.get(URL + "/page" + str(pageNumberToCrawl)).content, "html.parser")
    posts = page.find("ol", class_="posts").find_all("li", class_="postbitlegacy postbitim postcontainer old")
    crawledPosts[pageNumberToCrawl] = posts
    postIds =[post['id'] for post in page.find("ol", class_="posts").find_all("span", class_="fixscroll")]
    pageNumberToCrawl = int(pageNumberToCrawl)-1

# excluding posts crawled in the past
blackListedPostIds = postIds[0:postIds.index(lastIdCrawled)+1] 

# iterating over posts to send telegram message
for savedPage in reversed(crawledPosts):
    print("Sending messages for page number: " + str(savedPage))
    posts = crawledPosts[savedPage]
    for post in posts:
        try:
            if post.find("span", class_="fixscroll")['id'] in blackListedPostIds: continue
            sendMessage = []
            author = post.find("div", class_="popupmenu memberaction").find("strong").text
            if author == "3DGames": continue #exclude Ads
            datetime = post.find("div", class_="posthead").find("span", class_="date").text
            message = post.find("div", class_="content")
            quotes = message.find_all("div", class_="bbcode_container")
            sendMessage = datetime + " \n" + "Author: " + author

            if len(quotes) > 0:
                for quote in quotes:
                    sendMessage = sendMessage + "\n" + "Quoted message from:" + quote.find("div", class_="bbcode_postedby").find("strong").text
                    sendMessage = sendMessage + "\n" + '"' + quote.find("div", class_="message").text + '"'
                for quote in message("div", class_="bbcode_container"):
                    quote.decompose()

            images = message.find_all("img")
            links = message.find_all("a")

            sendMessage = sendMessage + "\n" + message.text
            if len(links) > 0:
                for link in links:
                    if isinstance(link, type(None)):
                        continue
                    sendMessage = sendMessage + "\n" + "Link:" + link["href"]

            params = {
                "chat_id": CHAT_ID,
                "text": sendMessage
            }
            results = requests.post(request_url + "/sendMessage", params= params)

            if len(images) > 0:
                arrayOfImages = []
                for image in images:
                    if isinstance(image, type(None)):
                        continue
                    if 'http' in image["src"]:
                        arrayOfImages.append({"type":"photo","media":image["src"]})
                if len(arrayOfImages) > 0:
                    params = {
                        "chat_id": CHAT_ID,
                        "media": json.dumps(arrayOfImages, separators=(',', ':')),
                        "reply_to_message_id" : int(results.json()['result']['message_id'])
                    }
                    results = requests.post(request_url + "/sendMediaGroup", params= params)

            time.sleep(SLEEP_TIME)
        except:
            continue
print("Saving last postId crawled...")
lastPostId = crawledPosts[lastThreadPageNumber][-1].find("span", class_="fixscroll")['id']
requests.put("https://jsonblob.com/api/jsonBlob/" + JSONBLOD_ID, json={'id':lastPostId})
    
print("Process finished")
