# -*- coding: utf-8 -*-
"""Web search in brave incognito mode
Synopsis: <trigger> <expression>"""

import time
import urllib

from albert import *

__title__ = "Web Search"
__version__ = "0.4.0"
__triggers__ = "!"
__authors__ = ["hankliao87"]

EXEC = "brave"

BANG_DICT = {
    "g": {"name": "Google", "url": "https://www.google.com/search?q={}"},
    "yt": {"name": "Youtube", "url": "https://www.youtube.com/results?search_query={}"},
    "gh": {"name": "GitHub", "url": "https://github.com/search?utf8=✓&q={}"},
    "=": {"name": "WolframAlpha", "url": "https://www.wolframalpha.com/input/?i={}"},
    "dd": {"name": "DuckDuckGo", "url": "https://duckduckgo.com/?q={}"},
}

iconPath = iconLookup(EXEC)

def handleQuery(query):
    if query.isTriggered:
        query_string = query.string.strip()

        if query_string == "":
            item = Item(id=__title__, icon=iconPath)
            item.text = "Search"
            return item
        else:
            try:
                query_list = query_string.split(" ", 1)

                if len(query_list) == 1:
                    bang = query_string
                    keyword = None
                else:
                    bang, keyword = query_list

                if BANG_DICT.get(bang, {}).get("name", None):
                    name = BANG_DICT[bang]["name"]
                    url = BANG_DICT[bang]["url"]
                else:
                    raise Exception("Service not found")

                if keyword:
                    # time.sleep(0.3) # avoid rate limiting
                    api_url = url.format(urllib.parse.quote_plus(keyword))

            except Exception as ex:
                item = Item(id=__title__, icon=iconPath)
                item.text = "Error: " + str(ex)
                item.addAction(ClipAction(text="Copy error message to clipboard", clipboardText=str(ex)))
                return item

            item = Item(id=__title__, icon=iconPath)
            if keyword:
                item.text = str(keyword)
                item.subtext = f"Search in {name}"
                item.addAction(ProcAction(text="Open in brave incognito mode", commandline=[EXEC, "-incognito", f"{api_url}"]))
                item.addAction(ProcAction(text="Open in brave normal mode", commandline=[EXEC, f"{api_url}"]))
                item.addAction(ClipAction(text="Copy url to clipboard", clipboardText=str(api_url)))
            else:
                item.text = f"Search in {name}"
            return item

