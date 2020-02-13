#!/usr/bin/env python3

import pywikibot

class Club():

    def __init__(self, site, url):
        self.site = site
        self.url = url
        self.page = pywikibot.Page(site, url).get()

    def getCurrentSaison(self):
        pass

    """get page text"""
    def get(self):
        return self.page
