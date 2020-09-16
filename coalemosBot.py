import re

import pywikibot

from scripts.updateUserContributionsBox import updateUserContributionsBox
from scripts.fixInternalLink import fixInternalLink
from scripts.startTranslate.handballPage import handballPage


class CoalemosBot():
    pages = []

    def __init__(self, site, pages = []):
        self.site = site
        for pageName in pages:
            self.pages.append(pywikibot.Page(self.site, pageName))

    def addCategory(self, catName):
        cat = pywikibot.Category(self.site, "Catégorie:" + catName)
        for page in cat.articles(recurse=False):
            self.pages.append(page)

    def addPage(self, pageName):
        self.pages.append(pywikibot.Page(self.site, pageName))

    def cleanDraft(self):
        self.updateDraft('')

    def fixInternalLink(self):
        for page in self.pages:
            # if the current page is already a redirection page
            while page.isRedirectPage():
                page = pywikibot.Page(self.site, page.getRedirectTarget().title())

            for pageRedirect in page.getReferences(filter_redirects=True):
                # print(pageRedirect.title())

                # print('Link : ')
                for pageWithRedirect in pageRedirect.getReferences():
                    print('-------------')
                    print('- page : ' + page.title())
                    print('- pageRedirect : ' + pageRedirect.title())
                    print('- pageWithRedirect : ' + pageWithRedirect.title())
                    fixInternalLink(pageWithRedirect.title())
                    # fixInternalLink(u'Utilisateur:CoalémosBot/Brouillon')



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

    def updateUserContibutions(self, username):
        updateUserContributionsBox(username)

    def translate(self, pageName):
        handballPage(pageName)


    def replaceModelDate(self, page):
        text = page.get()
        reg = r'({{date)\ssport\(|\d{1,2}\|\w+\|\d{4}\|en\s\w+}})'
        if (re.match(reg, text)):
            print('FOUND - ')
            print(page)
            # page = re.sub(reg, '$1$2', text)
