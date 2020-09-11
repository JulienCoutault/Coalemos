#!/usr/bin/env python3

import re

import pywikibot

class Club():
    def __init__(self, site, url):
        self.site = site
        self.url = url
        self.page = pywikibot.Page(site, url).get()

    def getCurrentSaison(self):
        return re.search("actualité\s*=\s+(.+)\n", self.page)[1]

    def getSaisons(self):
        pass

    """get page text"""
    def get(self):
        return self.page

    def getInfobox(self):
        return self.infobox
