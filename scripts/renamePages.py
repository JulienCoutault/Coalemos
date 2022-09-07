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

    category = 'Coupe_du_monde_des_clubs_de_handball'
    message = "Renommage"
    regexSearch = r'Coupe du monde des clubs de handball(\s\d{4})?'
    regexReplace = r'Coupe du monde des clubs masculins de handball'

    site = pywikibot.Site()
    site.login()
    
    pages = []
    for page in pywikibot.Category(site, "Catégorie:" + category).articles(recurse=True):
        #print(page.title)
        if page.botMayEdit() and re.search(regexSearch, page.title()):
            newTitle = re.sub(regexSearch, regexReplace, page.title())
            print('[{}] -> [{}]'.format(page.title(), newTitle))
            if args.work:
                if not args.force:
                    if input('Are you agree ? : ') == 'y':
                        page.move(newTitle, message)
                else:
                    page.move(newTitle, message)
    sys.exit(os.EX_OK)
