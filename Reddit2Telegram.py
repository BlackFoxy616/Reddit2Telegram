from __future__ import unicode_literals

import telegram
import praw
import logging
import html
import sys
import os
import json

from time import sleep
from datetime import datetime

credentials = {}

credentials["token"] = "5244169085:AAE3uFBJbv4S9a_w2ndkR7IvAlrgNR66b4M"
credentials["subreddit"] = "UHQDesi"
credentials["channel"] = "-1001478556147"

log = logging.getLogger('doggo')
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

if credentials["token"] == "": 
    raise RuntimeError('Bot token not found 馃檨! Put bot token馃攼 in credentials.json!')
if credentials["subreddit"] == "":
    raise RuntimeError('Subreddit name not found 馃檨! Enter the subreddit name馃搩 in credentials.json!')
if credentials["channel"] == "":
    raise RuntimeError('Telegram Channel name not found 馃檨! Enter the channel name馃摪 in credentials.json!')

token = credentials["token"]
channel = credentials["channel"]
sub = "LenaPaul"
start_time = datetime.utcnow().timestamp()

def prev_submissions():
    try:
        with open('prev_submissions.id', 'r') as f:
            return f.read().strip()
    except:
        return None

def write_submissions(sub_id):
    try:
        with open('prev_submissions.id', 'w') as f:
            f.write(sub_id)
    except:
        log.expection("Error writing sub ID!")

post = False
last_sub_id = prev_submissions()

if not last_sub_id:
    log.info("Latest submission not found, starting all submissions!")
    post = True
else:
    log.info("Last posted submission is {}".format(last_sub_id))

r = praw.Reddit(
    client_id="e7fk048oBQr7cr_5yc2bsQ",
    client_secret="OsjG-G_MgfzUIhWOuPlTC3mUO22ypw",
    password="hatelenovo@33",
    user_agent="testscript",
    username="puzzleheaded-bee8597",
)
r.read_only = True
subreddit = r.subreddit(sub)

bot = telegram.Bot(token=token)
# for submission in subreddit.stream.submissions():
#     print(submission.url)

while True:
    try:
        for submission in subreddit.hot():
            try:
                link = "https://redd.it/{id}".format(id=submission.id)
                if not post and submission.created_utc < start_time:
                    log.info("Skipping {} --- latest submission not found!".format(submission.id))
                    if submission.id == last_sub_id:
                        post = True
                    continue
                image = html.escape(submission.url or '')
                title = html.escape(submission.title or '')
                user = html.escape(submission.author.name or '')

                template = "{title}\n{link}\nby {user}"
                message = template.format(title=title, link=link, user=user)

                log.info("Posting {}".format(link))
                bot.sendPhoto(chat_id=channel, photo=submission.url, caption=message)
                # bot.sendMessage(chat_id=channel, parse_mode=telegram.ParseMode.HTML, text=message)
                write_submissions(submission.id)
                sleep(5)
            except Exception as e:
                log.exception("Error parsing {}".format(link))
    except Exception as e:
        log.exception("Error fetching new submissions, restarting in 10 secs")
        sleep(10)
