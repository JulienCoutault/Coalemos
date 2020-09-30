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

        if link[2] or 'masculin' in link[0] or 'féminin' in link[0]:
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
        if nbFix > 1:
            return 'Correction liens internes'
        else:
            return 'Correction lien interne'
