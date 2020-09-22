#!/usr/bin/env python3

import argparse
import os
import re
import sys

import pywikibot

def fixInternalLink(site, page):
    text = page.get()
    newText = text
    nbFix = 0
    for link in re.findall(r"\[\[([\-\'\w\dÀ-ÿ\s]+)(\|([\-\'\w\dÀ-ÿ\s]+))?\]\]", text, flags=re.IGNORECASE):
        pageLink = pywikibot.Page(site, link[0])
        if not pageLink.isRedirectPage():
            if link[2] and link[2] == link[0]:
                nbFix += 1
                newText = newText.replace('[[{}{}]]'.format(link[0], link[1]), '[[{}]]'.format(link[0]))
        else:
            while pageLink.isRedirectPage():
                pageLink = pywikibot.Page(site, pageLink.getRedirectTarget().title())
            if link[2] and pageLink.title() == link[2]:
                nbFix += 1
                newText = newText.replace('[[{}{}]]'.format(link[0], link[1]), '[[{}]]'.format(pageLink.title()))
            else:
                nbFix += 1
                newText = newText.replace('[[{}{}]]'.format(link[0], link[1]), '[[{}{}]]'.format(pageLink.title(), link[1]))

    if nbFix:
        pywikibot.showDiff(text, newText)
        if input('Are you agree ? : ') == 'y':
            page.text = newText
            if nbFix > 1:
                page.save('Correction liens internes', minor=True, botflag=True)
            else:
                page.save('Correction lien interne', minor=True, botflag=True)


def fixInternalLinkStr(pageName):
    site = pywikibot.Site()
    site.login()
    page = pywikibot.Page(site, pageName)
    return fixInternalLink(site, page)

def parse_args():
    parser = argparse.ArgumentParser(
        prog='fixInternalLink',
        description='Check internal link to replace redirection'
    )
    parser.add_argument('page', help='page to check')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    fixInternalLinkStr(args.page)

    sys.exit(os.EX_OK)
