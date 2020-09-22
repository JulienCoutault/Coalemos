from datetime import datetime, timedelta
import re
import sys

import pywikibot

from scripts.fixInternalLink import fixInternalLink
from scripts.fixModels import fixModels
from scripts.getUnusedRedirect import getUnusedRedirect
from scripts.updateUserContributionsBox import updateUserContributionsBox
from scripts.startTranslate.handballPage import handballPage


class CoalemosBot:
    pages = []

    def __init__(self, pages=[]):
        self.site = pywikibot.Site()
        self.site.login()

        for pageName in pages:
            self.addPage(pageName)

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

    def getUnusedRedirect(self):
        text = '\n'
        for page in self.pages:
            links = getUnusedRedirect(page.title())
            if links != []:
                text += "== [[{}]] ==\n".format(page.title())
                for link in links:
                    text += "* [[Spécial:Pages_liées/{}|{}]]\n".format(link,link)


        # update user page

        page = pywikibot.Page(self.site, u'Utilisateur:CoalémosBot/bot/UnusedRedirect')
        page.text = (re.sub('(<!-- BEGIN BOT SECTION -->)(\n|\s|.)*(<!-- END BOT SECTION -->)',
            r'\1\n{}\n\3'.format(text), page.text))
        page.save('([[bot]]) Mise a jour', minor=False, botflag=True)

    def fixInternalLinks(self):
        for page in self.pages:
            # if the current page is already a redirection page
            while page.isRedirectPage():
                page = pywikibot.Page(self.site, page.getRedirectTarget().title())

            fixInternalLink(self.site, page)

    def fixModels(self):
        for page in self.pages:
            # if the current page is already a redirection page
            while page.isRedirectPage():
                page = pywikibot.Page(self.site, page.getRedirectTarget().title())

            fixModels(page)

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

        brouillon.save('([[bot]]) ' + msg, minor=False, botflag=True)

    def updateUserContributionsBox(self):
        updateUserContributionsBox('Programmateur01')

    def translate(self, pageName):
        handballPage(pageName)
