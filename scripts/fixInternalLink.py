#!/usr/bin/env python3

import re

import pywikibot

def fixInternalLink(pageName):
    site = pywikibot.Site()
    site.login()
    page = pywikibot.Page(site, pageName)
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
        print(pywikibot.showDiff(text, newText))
        if input('Are you agree ?') == 'y':
            page.text = newText
            print('Validate')
            if nbFix > 1:
                page.save('Correction liens internes', minor=True, botflag=True)
            else:
                page.save('Correction lien interne', minor=True, botflag=True)


if __name__ == '__main__':
    pass
