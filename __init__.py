# -*- coding: utf-8 -*-

import time
import urllib
import urllib.parse

from albert import *

__doc__ = """
Web search in brave incognito mode
Synopsis: `<trigger> <expression>`
"""

md_iid = "0.5"
md_version = "0.1"
md_name = "Web Search"
md_description = "Web Search"
md_license = "MIT"
md_url = "https://github.com/hankliao87/albert-web-search"
md_maintainers = "@hankliao87"

trigger = "!"

EXEC = "brave"

BANG_DICT = {
    "g": {"name": "Google", "url": "https://www.google.com/search?q={}"},
    "yt": {"name": "Youtube", "url": "https://www.youtube.com/results?search_query={}"},
    "gh": {"name": "GitHub", "url": "https://github.com/search?utf8=✓&q={}"},
    "=": {"name": "WolframAlpha", "url": "https://www.wolframalpha.com/input/?i={}"},
    "dd": {"name": "DuckDuckGo", "url": "https://duckduckgo.com/?q={}"},
}


class Plugin(QueryHandler):
    iconPath = [f"xdg:{EXEC}"]

    def id(self):
        return __name__

    def name(self):
        return md_name

    def description(self):
        return md_description

    def synopsis(self) -> str:
        return "<name>"

    def defaultTrigger(self) -> str:
        return trigger

    def handleQuery(self, query):
        query_string = query.string.strip()

        if query_string == "":
            item = Item(id=__name__, icon=self.iconPath)
            item.text = "Search"
            query.add(item)
        else:
            try:
                query_list = query_string.split(" ", 1)

                if len(query_list) == 1:
                    bang = query_string

                    if bang == "?":
                        for key in sorted(BANG_DICT.keys()):
                            name = BANG_DICT[key]["name"]
                            item = Item(
                                id=__name__,
                                icon=self.iconPath,
                                text=f"{trigger}{key}",
                                subtext=f"Search in {name}",
                            )
                            query.add(item)

                    elif not query.string.endswith(" "):
                        filter_BANG = list(filter(lambda item: item.startswith(bang), BANG_DICT.keys()))
                        for key in sorted(filter_BANG):
                            name = BANG_DICT[key]["name"]
                            item = Item(
                                id=__name__,
                                icon=self.iconPath,
                                text=f"{trigger}{key}",
                                subtext=f"Search in {name}",
                            )
                            query.add(item)

                    else:
                        if BANG_DICT.get(bang, {}).get("name", None):
                            name = BANG_DICT[bang]["name"]
                            url = BANG_DICT[bang]["url"]
                        else:
                            raise Exception("Service not found")

                        item = Item(id=__name__, icon=self.iconPath)
                        item.text = f"Search in {name}"
                        query.add(item)

                else:
                    bang, keyword = query_list

                    if BANG_DICT.get(bang, {}).get("name", None):
                        name = BANG_DICT[bang]["name"]
                        url = BANG_DICT[bang]["url"]
                    else:
                        raise Exception("Service not found")

                    # time.sleep(0.3) # avoid rate limiting
                    api_url = url.format(urllib.parse.quote_plus(keyword))
                    item = Item(
                        id=__name__,
                        icon=self.iconPath,
                        text=str(keyword),
                        subtext=f"Search in {name}",
                        actions=[
                            Action(
                                id="open-incognito",
                                text="Open in incognito mode",
                                callable=lambda u=[EXEC, "-incognito", str(api_url)]: runDetachedProcess(u)),
                            Action(
                                id="open-normal",
                                text="Open in normal mode",
                                callable=lambda u=[EXEC, str(api_url)]: runDetachedProcess(u)),
                            Action(
                                id="copy-repo-url",
                                text="Copy repo url to clipboard",
                                callable=lambda u=api_url: setClipboardText(u)),
                        ]
                    )
                    query.add(item)

            except Exception as ex:
                item = Item(
                    id=__name__,
                    icon=self.iconPath,
                    actions=[
                        Action(
                            id="copy-clipboard",
                            text="Copy error message to clipboard",
                            callable=lambda u=str(ex): setClipboardText(u)),
                        Action(
                            id="copy-repo-url",
                            text="Copy repo url to clipboard",
                            callable=lambda: setClipboardText(md_url)),
                    ]
                )
                item.text = f"Error: {str(ex)}"
                item.subtext = f"Please create an issue in {md_url}"
                query.add(item)

