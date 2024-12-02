from selenium.webdriver.common.by import By

PROFILE_SECTEUR_TEXTS=['Secteur(s)',"Secteur d’activité"]

class YFProfileScraper:

    def __init__(self,profile_webdriver):
        self.profile={}
        self.profile_webdriver=profile_webdriver

    def get_profile(self):
        self.__get_name()
        for t in PROFILE_SECTEUR_TEXTS:
            self.__get_secteur_by_text(t)
        self.__get_website()

    def __get_name(self):
        try:
            self.profile['Nom']=self.profile_webdriver.find_element(By.XPATH,"//section[@data-testid='asset-profile']//h3").text
        except:
            self.profile['Nom']=''

    def __get_secteur_by_text(self,text):
        try:
            self.profile[text]=self.profile_webdriver.find_element(By.XPATH,"//span[text()='"+text+"']/following-sibling::span").text
        except:
            self.profile[text]=''

    def __get_website(self):
        try:
            self.profile['Website']=self.profile_webdriver.find_element(By.XPATH,"//div[@id='Main']//a[contains(@href,'https')]").get_attribute('href')
        except:
            self.profile['Website']=''

    def get_profile_by_title(self,title):
        try:
            return self.profile[title]
        except:
            return ''

    