#!/usr/bin/env python3

import re

import pywikibot

def getUnusedRedirect(pageName):
    site = pywikibot.Site()
    site.login()
    page = pywikibot.Page(site, pageName)
    # if the current page is already a redirection page
    while page.isRedirectPage():
        page = pywikibot.Page(self.site, page.getRedirectTarget().title())

    unuseRedirect = []
    for pageRedirect in page.getReferences(filter_redirects=True):
        if len(list(pageRedirect.getReferences())) == 0:
            # No link to this page
            unuseRedirect.append(pageRedirect.title())


    return unuseRedirect


if __name__ == '__main__':
    pass
