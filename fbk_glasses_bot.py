#!/usr/bin/env python3.11

import json
import logging
import os
import sys
import time

import praw
import prawcore

logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s")

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)


# load config


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
if not os.path.exists(CONFIG_PATH):
    _logger.error("Config file not found: %s", CONFIG_PATH)
    sys.exit(1)

with open(CONFIG_PATH, "r") as f:
    try:
        CONFIG = json.loads(f.read())
    except json.JSONDecodeError:
        _logger.exception("Config file is not valid JSON")
        sys.exit(1)

AUTHOR_LINK = f"u/{CONFIG['author']}"
CLIP_LINK = CONFIG.get("clip_link", "https://www.youtube.com/watch?v=lWVt0YnSYEY")
ERROR_SLEEP_TIME = CONFIG.get("error_sleep_time", 60)
STATE_LOG_INTERVAL = CONFIG.get("state_log_interval", 24 * 60 * 60)

if CONFIG.get("debug"):
    _logger.setLevel(logging.DEBUG)
    for logger_name in ("praw", "prawcore"):
        logging.getLogger(logger_name).setLevel(logging.DEBUG)


# copypasta text and keywords


FBK_COPYPASTA = f"""I gotchu
_Takes a deep breath_

[Glasses are really versatile. First, you can have glasses-wearing girls take them off and suddenly become beautiful, or have girls wearing glasses flashing those cute grins, or have girls stealing the protagonist's glasses and putting them on like, "Haha, got your glasses!" That's just way too cute! Also, boys with glasses! I really like when their glasses have that suspicious looking gleam, and it's amazing how it can look really cool or just be a joke. I really like how it can fulfill all those abstract needs. Being able to switch up the styles and colors of glasses based on your mood is a lot of fun too! It's actually so much fun! You have those half rim glasses, or the thick frame glasses, everything! It's like you're enjoying all these kinds of glasses at a buffet. I really want Luna to try some on or Marine to try some on to replace her eyepatch. We really need glasses to become a thing in hololive and start selling them for HoloComi. Don't. You. Think. We. Really. Need. To. Officially. Give. Everyone. Glasses?]({CLIP_LINK})


_this is a bot. by {AUTHOR_LINK}_"""
FBK_COPYPASTA_JP = f"""I gotchu
_Takes a deep breath_

[眼鏡っていうのは本当にめちゃめちゃ多様性があるんですよねまず眼鏡をかけている女の子が眼鏡を外して美少女だったりとか逆に眼鏡をかけてニコニコしてみたり主人公の眼鏡を奪って着けてる女子や｢うばっちゃったぞ☆｣みたいにかけてそれも凄いかわいいんですよねあとは眼鏡男子もねあの眼鏡があやしく光ったり逆光してる姿もいいですしかっこいいもかわいいもそしてギャグまで使い回せるってのはめちゃめちゃいいんですよねシチュエーションでも対応してできるところもめちゃめちゃいいんですよ多種多様な形とか色とかもそのキャラに合った眼鏡を着せ替えて楽しむのも本当に楽しいですアンダーリムとかねちょっと淵が太いやつとかね本当にヴァイキングのようにめちゃめちゃ楽しめるんですルーナちゃんにかけてみたりマリンちゃんも眼帯外してかけてみたりとかもうホロライブメガネはマジで流行ってほしいしホロコミに出すべきだし是非！公式から！みんなに！眼鏡を！付与して！ほしいと思わないかなぁ！？かけたいよね？]({CLIP_LINK})


_this is a bot. by {AUTHOR_LINK}_"""

KEYWORDS = ["glasses"]
KEYWORDS_JP = ["megane", "眼鏡", "メガネ", "めがね"]


# bot loop


def make_state():
    return {
        "log_time": time.time(),
        "submission_count": 0,
        "reply_count": 0,
    }


def check_keyword(content, keywords):
    alnum_parts = "".join((x if x.isalnum() else " ") for x in content.lower()).split()
    return any(
        (
            (word in alnum_parts)  # EN/romanji keywords
            if word.isascii()
            else any(word in part for part in alnum_parts)  # JP keywords
        )
        for word in keywords
    )


_logger.info("Starting")
reddit = praw.Reddit(
    user_agent=f"fbk_glasses_bot (by {AUTHOR_LINK})",
    client_id=CONFIG["client_id"],
    client_secret=CONFIG["client_secret"],
    username=CONFIG["username"],
    password=CONFIG["password"],
)
_logger.info("Logged in as: %r", reddit.user.me())

subreddit = reddit.subreddit("+".join(CONFIG["subreddits"]))
state = make_state()

while True:
    try:
        for submission in subreddit.stream.submissions(skip_existing=True):
            _logger.debug("%s: Title: %s", submission.permalink, submission.title)
            state["submission_count"] += 1

            # get text of the reply

            if check_keyword(submission.title, KEYWORDS):
                reply_text = FBK_COPYPASTA
            elif check_keyword(submission.title, KEYWORDS_JP):
                reply_text = FBK_COPYPASTA_JP
            else:
                reply_text = None

            # reply

            if reply_text:
                _logger.info("%s: Replying", submission.permalink)
                state["reply_count"] += 1

                if CONFIG.get("debug"):
                    _logger.debug(
                        "%s: Reply not posted in debug mode", submission.permalink
                    )
                else:
                    submission.reply(reply_text)

            # log number of processed submissions

            state_time_delta = int(time.time() - state["log_time"])
            if state_time_delta > STATE_LOG_INTERVAL:
                _logger.info(
                    "%s submissions and %s replies processed in last %s seconds",
                    state["submission_count"],
                    state["reply_count"],
                    state_time_delta,
                )
                state = make_state()

    except KeyboardInterrupt:
        _logger.info("Keyboard interrupt")
        break

    except (
        praw.exceptions.RedditAPIException,
        prawcore.exceptions.PrawcoreException,
    ) as e:
        # might be a rate limit or HTTP 500
        _logger.error(
            "API error! Will sleep for %ss. %s: %s",
            ERROR_SLEEP_TIME,
            e.__class__.__name__,
            e,
        )
        time.sleep(ERROR_SLEEP_TIME)

    except Exception:
        _logger.exception("Unexpected error! Will sleep for %ss.", ERROR_SLEEP_TIME)
        time.sleep(ERROR_SLEEP_TIME)
