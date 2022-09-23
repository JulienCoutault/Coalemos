#!/usr/bin/env python3

import argparse
import os
import re
import sys

import pywikibot


def parse_args():
    parser = argparse.ArgumentParser(
        prog='updateUserContributionsBox',
        description='Update the number of contributions in [[Modèle:Utilisateur Contributions]]'
    )
    
    parser.add_argument('-f', '--force', action='store_true', default=False, help="Work without verification")
    parser.add_argument('-w', '--work', action='store_true', default=False, help="Work (only show pages to process by default)")

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()

    category = 'Compétition de handball en Amérique'
    message = "Renommage"
    regexSearch = r"Championnat d'Amérique du Sud et centrale des clubs (masculin|féminin) de handball"
    regexReplace = r"Championnat d'Amérique du Sud et centrale des clubs \1s de handball"
    
    renamedPages = {}

    site = pywikibot.Site()
    site.login()
    
    pages = []
    for page in pywikibot.Category(site, "Catégorie:" + category).articles(recurse=True):
        #print(page.title)
        if page.botMayEdit() and re.search(regexSearch, page.title()):
            newTitle = re.sub(regexSearch, regexReplace, page.title())
            print('[{}] -> [{}]'.format(page.title(), newTitle))
            renamedPages[page.title()] = newTitle
            if args.work:
                if not args.force:
                    if input('Are you agree ? : ') == 'y':
                        page.move(newTitle, message)
                else:
                    page.move(newTitle, message)
    for page in renamedPages:
        print(page)
        print(renamedPages[page])

    sys.exit(os.EX_OK)
