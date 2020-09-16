#!/usr/bin/env python3

import re

import pywikibot

def fixInternalLink(pageName):
    site = pywikibot.Site()
    site.login()
    page = pywikibot.Page(site, pageName)
    text = page.get()
    reg = [
        (r'(Ligue des champions)\s+(de\shandball)\s+((masculin|féminin)e?)', r"\1 \4e de l'EHF"),
        (r'(coupe EHF)\sde\shandball\s+((masculin|féminin)e?)', r"Coupe de l'EHF \3e"),
        (r'((coupe|supercoupe)\s+([a-zÀ-ÖØ-öø-ÿ\'\s]+))\s+(de\shandball)\s+((masculin|féminin)e?)', r'\1 \6e \4'),
        (r'((championnat)\s+([a-zÀ-ÖØ-öø-ÿ\-\'\s]+))\s+(de\shandball)\s+((masculin|féminin)e?)(\sde\sD1)?', r'\1 \6 \4'),
        (r'((Équipe)\s+([a-zÀ-ÖØ-öø-ÿ\-\'\s]+))\s+(de\shandball)\s+((masculin|féminin)e?)', r'\2 \3 \6e \4')
    ]
    for r in reg:
        text = re.sub(r[0], r[1], text, flags=re.IGNORECASE)
    page.text = text
    page.save('([[bot]]) Correction redirections', minor=True, botflag=True)


if __name__ == '__main__':
    pass
