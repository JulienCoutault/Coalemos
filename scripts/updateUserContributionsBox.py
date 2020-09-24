#!/usr/bin/env python3

import argparse
import os
import re
import sys

import pywikibot


def updateUserContributionsBox(username, force=False):
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
    newText = re.sub(re.escape(box), newBox, text, flags=re.IGNORECASE)
    userPage.text = newText
    if box != newBox:
        # Need an update
        if not force:
            pywikibot.showDiff(text, newText)
            if input('Are you agree ? : ') == 'y':
                userPage.save('Mise à jour de [[Modèle:Utilisateur Contributions]]', minor=True, botflag=True)
        else:
            userPage.save('Mise à jour de [[Modèle:Utilisateur Contributions]]', minor=True, botflag=True)


def parse_args():
    parser = argparse.ArgumentParser(
        prog='updateUserContributionsBox',
        description='Update the number of contributions in [[Modèle:Utilisateur Contributions]]'
    )
    parser.add_argument('user', help='User to update the contributions')
    parser.add_argument('-f', '--force', action='store_true', default=False, help="Work without verification")

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    updateUserContributionsBox(args.user, args.force)

    sys.exit(os.EX_OK)
