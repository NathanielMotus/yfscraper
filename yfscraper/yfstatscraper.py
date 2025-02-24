from selenium.webdriver.common.by import By
import selenium.common.exceptions
from yfscraper import yfutilities

STATISTICS_TEXTS=('Actions en attente',
                  'Flottant',
                  'Rendement en dividendes moyen')

class YFStatScraper:

    def __init__(self,stat_webdriver) -> None:
        self.statistics={}
        self.stat_webdriver=stat_webdriver

    def get_statistics(self):
        self.__get_market_price()
        for t in STATISTICS_TEXTS:
            self.__get_stat_by_text(t)
    
    def __get_market_price(self):
        try:
            #self.statistics['Cours']=float(self.stat_webdriver.find_element(By.XPATH,'//*[@data-testid="qsp-price" and @data-field="regularMarketPrice"]').get_attribute('data-value'))
            self.statistics['Cours']=yfutilities.parse_stat_number(self.stat_webdriver.find_element(By.XPATH,'//*[@data-testid="qsp-price"]'))
        except:
            self.statistics['Cours']=0

    def __get_stat_by_text(self,text):
        try:
            # localise la racine
            #historique
            #root=self.stat_webdriver.find_element(By.XPATH,"//span[contains(text(),'"+text+"')]").find_element(By.XPATH,"..").find_element(By.XPATH,"..")
            #30/11/24 :
            root=self.stat_webdriver.find_element(By.XPATH,"//td[contains(text(),'"+text+"')]").find_element(By.XPATH,"..")
            # récupère la valeur de la stat
            #self.statistics[text]=yfutilities.parse_stat_number(root.find_elements(By.XPATH,'.//*[text()!=""]')[-1])
            #30/11/24
            self.statistics[text]=yfutilities.parse_stat_number(root.find_elements(By.XPATH,'.//*[text()!=""]')[-1])
        except:
            self.statistics[text]=0

    # renvoie la valeur de la clé
    def get_stat_by_title(self,title):
        try:
            return self.statistics[title]
        except:
            return 0