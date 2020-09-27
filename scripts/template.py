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
                if template.name not in modelsChange:
                    modelsChange.append(str(template.name))

    if modelsChange:
        if len(modelsChange) == 1:
            msg = "Correction du modèle " + modelsChange[0]
        else:
            msg = "Correction des modèles " + str(modelsChange).strip('[]').replace("'", '')
        page.text = newText

        return msg

def formatTemplate(text, template):
    listParams = []
    maxLengthParam = 0

    # cut the model
    for line in template.params:
        param, value = re.findall(r'^([^=]*)=(.*)?$', line.strip())[0]
        param = param.strip()
        if len(param) > maxLengthParam:
            maxLengthParam = len(param)
        listParams.append([param, value.strip()])

    # build the model
    params = []
    for line in listParams:
        params.append(' {}{} = {}\n'.format(line[0], ' ' * (maxLengthParam - len(line[0])), line[1]))

    newTemplate = mwparserfromhell.nodes.template.Template(template.name, params)

    text.replace(template, newTemplate)

def fixInfobox_Competition_sportive(newText, template):
    change = False
    commonMistake = {
        "relégués": "relégué fin",
        "promus début": "promu début"
    }
    if template.has("date", True):
        # page for one edition
        if template.has("éditions", True):
            # param doesn't exist, judge it's a typo for édition
            change = True
            template.add('édition', template.get("éditions").value.strip(), before="éditions")
            template.remove("éditions")
        if not template.has("édition", True) and template.has("nombre d'éditions", True):
            # judge it's a mistake with édition
            change = True
            template.add('édition', template.get("nombre d'éditions").value.strip(), before="nombre d'éditions")
            template.remove("nombre d'éditions")
    else:
        # resume page for all editions
        if template.has("éditions", True):
            # param doesn't exist, judge it's a typo for nombre d'éditions
            change = True
            template.add("nombre d'éditions", template.get("éditions").value.strip(), before="éditions")
            template.remove("éditions")

    for mistake in commonMistake:
        if template.has(mistake, True):
            change = True
            template.add(commonMistake[mistake], template.get(mistake).value.strip(), before=mistake)
            template.remove(mistake)

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
