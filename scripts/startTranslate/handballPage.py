#!/usr/bin/env python3

import re

import pywikibot


def handballPage(pageName, lang = 'en'):
    site = pywikibot.Site();
    siteEn = pywikibot.Site(lang);
    page = pywikibot.Page(siteEn, pageName)
    text = page.get()
    textArr = text.split('\n')
    for t in textArr:
        print(t)


if __name__ == '__main__':
    pass