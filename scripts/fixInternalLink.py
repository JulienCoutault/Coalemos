#!/usr/bin/env python3

import argparse
import os
import re
import sys

import pywikibot

def fixInternalLink(site, page, force=False):
    text = page.get()
    newText = text
    nbFix = 0
    for link in re.findall(r"\[\[([\-\'\w\dÀ-ÿ\s:\/\(\)]+)(\|([\-\'\w\dÀ-ÿ\s\(\)]+))?\]\]", text, flags=re.IGNORECASE):
        link = list(link)
        if link[0].startswith(' ') or link[0].endswith(' '):
            # Remove useless space
            nbFix += 1
            newLink=  link[0].strip()
            newText = newText.replace('[[{}{}]]'.format(link[0], link[1]), '[[{}{}]]'.format(newLink, link[1]))
            link[0] = newLink

        if link[2]:
            # fix redirect only if target is specify
            pageLink = pywikibot.Page(site, link[0])
            if not pageLink.isRedirectPage():
                if link[2].capitalize() == link[0].capitalize():
                    # if the target is the same as the name
                    nbFix += 1
                    newText = newText.replace('[[{}{}]]'.format(link[0], link[1]), '[[{}]]'.format(link[2]))
            else:
                while pageLink.isRedirectPage():
                    pageLink = pywikibot.Page(site, pageLink.getRedirectTarget().title())
                if pageLink.title().capitalize() == link[2].capitalize():
                    # if the target is the same as the name
                    nbFix += 1
                    newText = newText.replace('[[{}{}]]'.format(link[0], link[1]), '[[{}]]'.format(pageLink.title()))
                else:
                    nbFix += 1
                    newText = newText.replace('[[{}{}]]'.format(link[0], link[1]), '[[{}{}]]'.format(pageLink.title(), link[1]))

    if nbFix:
        page.text = newText
        if not force:
            pywikibot.showDiff(text, newText)
            if input('Are you agree ? : ') == 'y':
                if nbFix > 1:
                    page.save('Correction liens internes', minor=True, botflag=True)
                else:
                    page.save('Correction lien interne', minor=True, botflag=True)
        else:
            if nbFix > 1:
                page.save('Correction liens internes', minor=True, botflag=True)
            else:
                page.save('Correction lien interne', minor=True, botflag=True)


def fixInternalLinkStr(pageName, force=False):
    site = pywikibot.Site()
    site.login()
    page = pywikibot.Page(site, pageName)
    return fixInternalLink(site, page, force)


def parse_args():
    parser = argparse.ArgumentParser(
        prog='fixInternalLink',
        description='Check internal link to replace redirection'
    )
    parser.add_argument('page', help='page to check')
    parser.add_argument('-f', '--force', action='store_true', default=False, help="Work without verification")

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    fixInternalLinkStr(args.page, args.force)

    sys.exit(os.EX_OK)
