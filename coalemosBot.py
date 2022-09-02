from datetime import datetime, timedelta
import re
import sys

import pywikibot

from scripts.fixInternalLink import fixInternalLink
from scripts.template import fixTemplates


class CoalemosBot:
    pages = []
    force = False

    def __init__(self, args, pages=[]):
        self.site = pywikibot.Site()
        self.site.login()
        self.args = args

        for pageName in pages:
            self.addPage(pageName)

    def run(self):
        for page in self.pages:
            msg = None
            # if the current page is already a redirection page
            while page.isRedirectPage():
                page = pywikibot.Page(self.site, page.getRedirectTarget().title())

            text = page.text
            if self.args.fixTemplates or self.args.all:
                msg = fixTemplates(page)

            if msg:
                if self.args.fixInternalLinks or self.args.all:
                    msg2 = fixInternalLink(self.site, page, self.force)
                    if msg2:
                        msg += ' + ' + msg2
                pywikibot.showDiff(text, page.text)
                print(msg)
                if self.args.force or input('Are you agree ? : ') == 'y':
                    page.save(msg, botflag=True)

    def addCategory(self, catName):
        cat = pywikibot.Category(self.site, "Catégorie:" + catName)
        for page in cat.articles(recurse=True):
            if page.userName() != 'CoalémosBot':
                self.pages.append(page)

    def addPage(self, pageName):
        page = pywikibot.Page(self.site, pageName)
        if page.userName() != 'CoalémosBot':
            self.pages.append(page)

    def cleanDraft(self):
        self.updateDraft('')

    def fixInternalLinks(self):
        for page in self.pages:
            # if the current page is already a redirection page
            while page.isRedirectPage():
                page = pywikibot.Page(self.site, page.getRedirectTarget().title())

            fixInternalLink(self.site, page, self.force)

    def get(self, title):
        self.title = title
        self.page = pywikibot.Page(self.site, title)
        return self.page

    def getModel(self, title):
        return self.get('Modèle:' + title)

    def updateDraft(self, text, msg = 'Mis a jour du brouillon'):
        brouillon = pywikibot.Page(self.site, u'Utilisateur:CoalémosBot/Brouillon')

        brouillon.text = '{{brouillon|{{BASEPAGENAME}}}}\n'
        brouillon.text += text
        brouillon.text += '\n{{page personnelle}}'

        brouillon.save(msg, minor=False, botflag=True)

    def updateUserContributionsBox(self):
        updateUserContributionsBox('Programmateur01', self.force)

    def translate(self, pageName):
        handballPage(pageName)
