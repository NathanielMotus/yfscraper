from selenium.webdriver.common.by import By

PROFILE_SECTEUR_TEXTS=["Secteur","Secteur d’activité"]

class YFProfileScraper:

    def __init__(self,profile_webdriver):
        self.profile={}
        self.profile_webdriver=profile_webdriver

    def get_profile(self):
        self.__get_name()
        self.__get_secteur()
        self.__get_secteur_activite()
        self.__get_website()

    def __get_name(self):
        try:
            self.profile['Nom']=self.profile_webdriver.find_element(By.XPATH,"//section[@data-testid='asset-profile']//h3").text
        except:
            self.profile['Nom']=''

    def __get_secteur(self):
        try:
            temp_webdriver=self.profile_webdriver.find_element(By.XPATH,"//dl[contains(@class,'company-stats')]//dt[contains(text(),'Secteur')]//following-sibling::dd")
            self.profile["Secteur"]=temp_webdriver.find_element(By.XPATH,'./strong').text
        except:
            self.profile["Secteur"]=''

    def __get_secteur_activite(self):
        try:
            self.profile["Secteur d’activité"]=self.profile_webdriver.find_element(By.XPATH,"//dl[contains(@class,'company-stats')]//dt[contains(text(),'Secteur d’activité')]//following-sibling::strong").text
        except:
            self.profile["Secteur d’activité"]=''


    def __get_website(self):
        try:
            self.profile['Website']=self.profile_webdriver.find_element(By.XPATH,"//main//a[contains(@href,'https')]").get_attribute('href')
        except:
            self.profile['Website']=''

    def get_profile_by_title(self,title):
        try:
            return self.profile[title]
        except:
            return ''

    