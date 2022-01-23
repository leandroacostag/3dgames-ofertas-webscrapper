# 3dgames-ofertas-webscrapper

This script is basically a webscrapper that crawls posts from a famous forum thread full of internet offers. Then this posts are sent to a telegram channel so it's easy to read over any device.

# Instructions
1. Install beautifulsoup4 library (pip install beautifulsoup4).
2. Create your own bot from the telegram BOT helper. https://core.telegram.org/bots#6-botfather
3. Create a telegram channel and take note of chatId.
4. Edit index.py with your own bot token and chatId.
5. You must set the oldest postId you want to crawl on the 'lastPostIdCrawled.txt' file. (This will determine how long it will take your first run). 

NOTE: you might want to create a cronjob to run this automatically every hour or so. Try here: https://www.geeksforgeeks.org/how-to-setup-cron-jobs-in-ubuntu/
