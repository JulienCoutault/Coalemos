#!/usr/bin/env python3

import argparse
import os
import re
import sys

import pywikibot
import mwparserfromhell


def fixTemplates(page):
    modelsChange = []
    text = page.get()
    newText = mwparserfromhell.parse(text)
    for template in newText.filter_templates():
        if template.name.matches("Infobox Compétition sportive"):
            if fixInfobox_Competition_sportive(newText, template):
                name = str(template.name).strip()
                if name not in modelsChange:
                    modelsChange.append(name)
        elif template.name.matches("Feuille de match handball"):
            if fixFeuille_de_match_handball(newText, template):
                name = str(template.name).strip()
                if name not in modelsChange:
                    modelsChange.append(name)

    if modelsChange:
        if len(modelsChange) == 1:
            msg = "Correction du modèle " + modelsChange[0]
        else:
            msg = "Correction des modèles " + ", ".join(modelsChange)
        page.text = newText

        return msg

def formatTemplate(text, template):
    listParams = []
    maxLengthParam = 0

    # cut the model
    for line in template.params:
        param = str(line.name).strip()
        value = str(line.value).strip()
        if len(param) > maxLengthParam:
            maxLengthParam = len(param)
        listParams.append([param, value.strip()])

    # build the model
    newTemplate = mwparserfromhell.nodes.template.Template(template.name)
    params = []
    for param in listParams:
        newTemplate.add(' {}{}'.format(param[0].strip(), ' ' * (maxLengthParam - len(param[0]) + 1)), " "+param[1]+"\n", preserve_spacing=False)

    text.replace(template, newTemplate)

################
# MODELS FIXES #
################
def fixFeuille_de_match_handball(newText, template):
    change = False
    commonMistake = {
        "arbitre": "arbitres",
        "Heure": "heure",
        "mi-temps": "score mi-temps",
        "SCORE MI-TEMPS": "score mi-temps",
        "stade": "lieu",
        "stadium": "lieu",
    }
    for param in template.params:
        name = str(param.name).strip()
        value = str(param.value).strip()
        if name in commonMistake:
            change = True
            template.add(commonMistake[name], value, before=name)
            template.remove(name)

    formatTemplate(newText, template)
    return change

def fixInfobox_Competition_sportive(newText, template):
    change = False
    commonMistake = {
        "relégués": "relégué fin",
        "promus début": "promu début"
    }
    for param in template.params:
        name = str(param.name).strip()
        value = str(param.value).strip()
        if name == "éditions":
            if template.has("date", True):
                # page for one edition
                # param doesn't exist, judge it's a typo for édition
                change = True
                template.add('édition', value, before=name)
                template.remove(name)
            else:
                # resume page for all editions
                # param doesn't exist, judge it's a typo for nombre d'éditions
                change = True
                template.add("nombre d'éditions", value, before=name)
                template.remove(name)
        elif name == "nombre d'éditions":
            if template.has("date", True):
                # page for one edition
                if not template.has("édition", True):
                    # judge it's a mistake with édition
                    change = True
                    template.add('édition', value, before=name)
                    template.remove(name)
        elif name in commonMistake:
            change = True
            template.add(commonMistake[name], value, before=name)
            template.remove(name)

    formatTemplate(newText, template)
    return change


def main(args):
    site = pywikibot.Site()
    site.login()
    page = pywikibot.Page(site, args.page)
    text = page.text
    msg = fixTemplates(page)

    pywikibot.showDiff(text, page.text)
    if msg and (args.force or input('Are you agree ? : ') == 'y'):
        page.save(msg, botflag=True)


def parse_args():
    parser = argparse.ArgumentParser(
        prog='Template',
        description='Check template in page'
    )
    parser.add_argument('page', help='page to check')
    parser.add_argument('-f', '--force', action='store_true', default=False, help="Work without verification")

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main(parse_args())

    sys.exit(os.EX_OK)
