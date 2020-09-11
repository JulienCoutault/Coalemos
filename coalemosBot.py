import re

import pywikibot

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

    def cleanRedirect(self):
        for page in self.pages:
            print('-------------')
            print(page.title())
            # if the current page is already a redirection page
            while page.isRedirectPage():
                page = pywikibot.Page(self.site, page.getRedirectTarget().title())

            for pageRef in page.getReferences(filter_redirects=True):
                print(pageRef.title())
                print('Model : ')
                for pageToRedirect in pageRef.getReferences(only_template_inclusion=True):
                    print('- '+pageToRedirect.title())
                    text = pageToRedirect.get()
                    self.updateDraft(text, '[[{}]] Copie'.format(pageToRedirect.title()))
                    text = re.sub(r'{{' + pageRef.title(with_ns=False), r'{{' + page.title(with_ns=False), text, flags=re.IGNORECASE)
                    self.updateDraft(text, '[[{}]] cleanRedirect'.format(pageToRedirect.title()))

                print('Link : ')
                for pageToRedirect in pageRef.getReferences():
                    print('- '+pageToRedirect.title())
                    text = pageToRedirect.get()
                    self.updateDraft(text, '[[{}]] Copie'.format(pageToRedirect.title()))
                    text = re.sub(r'\[\[' + pageRef.title(with_ns=False), '[[' + page.title(with_ns=False), text, flags=re.IGNORECASE)
                    self.updateDraft(text, '[[{}]] cleanRedirect'.format(pageToRedirect.title()))


    def get(self, title):
        self.title = title;
        self.page = pywikibot.Page(self.site, title)
        return self.page

    def getModel(self, title):
        return self.get('Modèle:' + title)

    def updateDraft(self, text, msg = 'Mis a jour du brouillon'):
        brouillon = pywikibot.Page(self.site, u'Utilisateur:CoalémosBot/Brouillon')

        brouillon.text = '{{brouillon|{{BASEPAGENAME}}}}\n'
        brouillon.text += text
        brouillon.text += '\n{{page personnelle}}'

        brouillon.save('([[bot]]) ' + msg, botflag=True)

    def translate(self, title):
        text = pywikibot.Page(self.site, title).get()


    def replaceModelDate(self, page):
        text = page.get()
        reg = r'({{date)\ssport\(|\d{1,2}\|\w+\|\d{4}\|en\s\w+}})'
        if (re.match(reg, text)):
            print('FOUND - ')
            print(page)
            # page = re.sub(reg, '$1$2', text)
