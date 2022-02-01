# 3dgames-ofertas-webscrapper

This script is basically a webscrapper that crawls posts from a famous forum thread full of internet offers and sends them to a telegram channel for easy consuming.
You can try it out here: https://t.me/+vLDTBoowBLJhOWYx

Forum thread URL: https://foros.3dgames.com.ar/threads/942062-ofertas-online-argentina/

# Instructions
1. Install beautifulsoup4 and requests libraries: `pip install beautifulsoup4 requests`
2. Create your own bot from the telegram BOT helper. https://core.telegram.org/bots#6-botfather
3. Create a telegram channel and take note of chatId.
4. Go to https://jsonblob.com/ and create a new json object as {"id":"postId"} with the oldest postId you want to crawl. (This will determine how long it will take your first run, you can get this). 
5. Edit main.py with your own bot token, chatId and jsonblob Id.
6. Run `python main.py` over your terminal to start running the process.

NOTE: you might want to create a cronjob to run this automatically every hour or so.

NOTE2: get your desired postId by inspecting the forum source code, you should look for something like this: `<span class="fixscroll" id="post23909652"></span>`
