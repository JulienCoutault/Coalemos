#!/usr/bin/env python3

import argparse
import os
import re
import sys

import pywikibot
import mwparserfromhell


def fixModels(page):
    msgSave = False
    text = page.get()
    newText = mwparserfromhell.parse(text)
    for template in newText.filter_templates():
        if template.name.matches("Infobox Compétition sportive") and template.has("date", True) and not template.has("édition", True) and (template.has("nombre d'éditions", True) or template.has("éditions", True)):
            template.add('édition', template.get("nombre d'éditions").value.strip(), before="nombre d'éditions")
            template.remove("nombre d'éditions")
            formatTemplate(newText, template)
            msgSave = "Correction de l'attribut édition dans Infobox Compétition sportive"

    if msgSave:
        pywikibot.showDiff(text, newText)
        if input('Are you agree ? : ') == 'y':
            page.text = newText
            page.save(msgSave, botflag=True)


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


def fixModelsStr(pageName):
    site = pywikibot.Site()
    site.login()
    page = pywikibot.Page(site, pageName)
    return fixModels(page)


def parse_args():
    parser = argparse.ArgumentParser(
        prog='fixModel',
        description='Check models in page'
    )
    parser.add_argument('page', help='page to check')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()

    fixModelsStr(args.page)

    sys.exit(os.EX_OK)
