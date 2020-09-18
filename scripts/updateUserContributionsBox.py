#!/usr/bin/env python3

import argparse
import os
import re
import sys

import pywikibot


def updateUserContributionsBox(username):
    site = pywikibot.Site()
    site.login()
    user = pywikibot.User(site, username)
    userPage = user.getUserPage()
    text = user.get()
    contributions = user.editCount()
    if contributions < 2000:
        contributions = contributions - contributions % 100
    else:
        contributions = contributions - contributions % 1000

    regexBox = r'{{Utilisateur Contributions\|\d+}}'
    box = re.search(regexBox, text, flags=re.IGNORECASE).group(0)
    newBox = '{{Utilisateur Contributions|'+str(contributions)+'}}'
    if box != newBox:
        # Need an update
        userPage.text = re.sub(re.escape(box), newBox, text, flags=re.IGNORECASE)
        userPage.save('Mise à jour de [[Modèle:Utilisateur Contributions]]', minor=True, botflag=True)


def parse_args():
    parser = argparse.ArgumentParser(
        prog='updateUserContributionsBox',
        description='Update the number of contributions in [[Modèle:Utilisateur Contributions]]'
    )
    parser.add_argument('user', help='User to update the contributions')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    updateUserContributionsBox(args.user)

    sys.exit(os.EX_OK)
