import re
import sys

import pywikibot

from scripts.fixInternalLink import fixInternalLink
from scripts.getUnusedRedirect import getUnusedRedirect
from scripts.updateUserContributionsBox import updateUserContributionsBox
from scripts.startTranslate.handballPage import handballPage


class CoalemosBot():
    pages = []
    nbPage = 0

    def __init__(self, pages = []):
        self.site = pywikibot.Site();
        self.site.login()

        print(self.nbPage)
        for pageName in pages:
            self.nbPage += 1
            sys.stdout.write("\033[F")
            print(self.nbPage)
            self.pages.append(pywikibot.Page(self.site, pageName))

    def addCategory(self, catName):
        cat = pywikibot.Category(self.site, "Catégorie:" + catName)
        for page in cat.articles(recurse=True):
            self.nbPage += 1
            sys.stdout.write("\033[F")
            print(self.nbPage)
            self.pages.append(page)

    def addPage(self, pageName):
        self.pages.append(pywikibot.Page(self.site, pageName))

    def cleanDraft(self):
        self.updateDraft('')

    def getUnusedRedirect(self):
        text = '\n'
        i = 0
        for page in self.pages:
            i += 1
            sys.stdout.write("\033[F")
            print("({}/{}) {}                              ".format(i, self.nbPage, page.title()))
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

            for pageRedirect in page.getReferences(filter_redirects=True):
                for pageWithRedirect in pageRedirect.getReferences():
                    fixInternalLink(pageWithRedirect.title())


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
