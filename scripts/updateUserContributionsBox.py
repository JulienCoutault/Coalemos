#!/usr/bin/env python3

import re

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
        # print(userPage.text)
        userPage.save('Mise à jour de [[Modèle:Utilisateur Contributions]]', minor=True, botflag=True)
    else:
        print('{} contributionsBox already up to date'.format(username))


if __name__ == '__main__':
    pass