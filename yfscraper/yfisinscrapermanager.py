import requests
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FFService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException
from selenium.webdriver import FirefoxOptions
from yfscraper.yfbalancesheetscraper import YFBalanceSheetScraper
from yfscraper.yfstatscraper import YFStatScraper
from yfscraper.yfprofilescraper import YFProfileScraper

YF_URL_LOOKUP="https://fr.finance.yahoo.com"
YF_URL_ROOT="https://fr.finance.yahoo.com/quote/"
YF_URL_BALANCE_SHEET_SUFFIX="/balance-sheet"
YF_URL_STAT_SUFFIX="/key-statistics"
YF_URL_PROFILE_SUFFIX="/profile"
#UBLOCK_EXTENSION_PATH_FF="D:\\Dossier Nanat\\31-Python\\yfscraper\\yfscraper\\extensions\\ublock_origin-1.57.2.xpi"
UBLOCK_EXTENSION_PATH_FF="D:\\Dossier Nanat\\31-Python\\yfscraper\\yfscraper\\extensions\\uBlock0_1.63.2.firefox.signed.xpi"
UBLOCK_EXTENSION_PATH_CHROME="D:\\Dossier Nanat\\31-Python\\yfscraper\\yfscraper\\extensions\\ublock_origin-1.61.2.crx"


class YFISINScraperManager:
    is_driver_started=False
    counter=0
    #Chrome
    #options=webdriver.ChromeOptions()
    #options.add_extension(UBLOCK_EXTENSION_PATH_CHROME)
    #options.add_argument("--start-maximized")
    #options.add_argument("-headless")

    #Firefox
    options=webdriver.FirefoxOptions()
    options.add_argument("--headless")
    #driver=webdriver.Firefox(service=FFService(),options=options)
        
    def __init__(self,yf_ISIN,reject_counter) -> None:
        self.yf_ISIN=yf_ISIN
        self.yf_ticker=''
        self.rejected_isin=''
        self.reject_counter=reject_counter

        # si le reject_counter est nul est que le driver est démarré, on l'arrête
        if self.reject_counter==0:
            YFISINScraperManager.driver.quit()
            YFISINScraperManager.is_driver_started=False
        
        # démarre yf et accepte les cookies si ce n'est pas déjà fait
        if not YFISINScraperManager.is_driver_started:
            self.__start_driver()
        YFISINScraperManager.driver.get(YF_URL_LOOKUP)

        # récupère le ticker
        self.__get_ticker_by_ISIN()

        # si ça ne répond pas, on récupère l'erreur en bas
        try:
        # si le ticker n'est pas vide, récupère les infos
            if self.yf_ticker!='':
                
             # instancie yf_stat_scraper
                YFISINScraperManager.counter+=1
                print(format(YFISINScraperManager.counter)+" "+self.yf_ticker)
                YFISINScraperManager.driver.get(YF_URL_ROOT+self.yf_ticker+YF_URL_STAT_SUFFIX)
                self.yf_stat_scraper=YFStatScraper(YFISINScraperManager.driver)
                # charge yf_stat_scraper
                self.yf_stat_scraper.get_statistics()

                # instancie yf_balance_sheet_scraper
                YFISINScraperManager.driver.get(YF_URL_ROOT+self.yf_ticker+YF_URL_BALANCE_SHEET_SUFFIX)
                # clique le bouton 'Trimestriel'
                self.__wait_and_click_button_by_title('Trimestriel')
                # clique le bouton 'tout développer'
                self.__wait_and_click_button_by_text('Développer tout')
                self.yf_balance_sheet_scraper=YFBalanceSheetScraper(YFISINScraperManager.driver)
                # charge yf_balance_sheet_scraper
                self.yf_balance_sheet_scraper.get_balance_sheet()

                #instancie yf_profile_scraper
                YFISINScraperManager.driver.get(YF_URL_ROOT+self.yf_ticker+YF_URL_PROFILE_SUFFIX)
                self.yf_profile_scraper=YFProfileScraper(YFISINScraperManager.driver)
                self.yf_profile_scraper.get_profile()

                # penser à quitter le driver quand c'est fini
                #self.driver.quit
        except:
            YFISINScraperManager.driver.quit
            YFISINScraperManager.is_driver_started=False
            self.rejected_isin=self.yf_ISIN

    def __start_driver(self):
        YFISINScraperManager.driver=webdriver.Firefox(options=YFISINScraperManager.options)
        #YFISINScraperManager.driver=webdriver.Chrome(options=YFISINScraperManager.options)
        YFISINScraperManager.driver.maximize_window()
        YFISINScraperManager.driver.set_window_size(1920,1080)
        YFISINScraperManager.driver.install_addon(UBLOCK_EXTENSION_PATH_FF,temporary=True)

        try:
            YFISINScraperManager.driver.get(YF_URL_LOOKUP)
            YFISINScraperManager.is_driver_started=True


            # démarre le driver sur une page vierge
            # wait up to 3 seconds for the consent modal to show up
            consent_overlay = WebDriverWait(YFISINScraperManager.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'consent-overlay')))
    
            # click "scroll down" button
            #scroll_down_button=consent_overlay.find_element(By.ID,'scroll-down-btn')
            #scroll_down_button.click()

            # click the "Accept all" button
            accept_all_button = consent_overlay.find_element(By.NAME, 'agree')
            accept_all_button.click()
        except TimeoutException:
            print('Cookie consent overlay missing')

    def __wait_and_click_button_by_text(self,button_text):
        try:
            # attends que le bouton soit cliquable
            button=WebDriverWait(YFISINScraperManager.driver,10).until(
                EC.element_to_be_clickable((By.XPATH,"//button/span[text()='"+button_text+"']"))
            )

            # clique le bouton
            button.click()

        except TimeoutException:
            print("Pas de bouton")

        except:
            print("Problème inconnu")

    def __wait_and_click_button_by_title(self,button_title):
        try:
            # attends que le bouton soit cliquable
            button=WebDriverWait(YFISINScraperManager.driver,10).until(
                EC.element_to_be_clickable((By.XPATH,"//button[@title='"+button_title+"']"))
            )

            # clique le bouton
            #curieusement, il faut cliquer 2 fois pour que ça fonctionne...
            button.click()
            button.click()

        except TimeoutException:
            print("Pas de bouton")

        except:
            print("Problème inconnu")

    def __get_ticker_by_ISIN(self):
        try:
            # attend 3 s qu'apparaisse la barre de recherche
            search_box = WebDriverWait(YFISINScraperManager.driver, 3).until(
                #historique des tags
                #EC.presence_of_element_located((By.ID, 'yfin-usr-qry')))
                #modif du 30/11/24 :
                EC.presence_of_element_located((By.ID, 'ybar-sbq')))
            search_box.send_keys(self.yf_ISIN)
            search_result=WebDriverWait(YFISINScraperManager.driver,3).until(
                #historique
                #EC.presence_of_element_located((By.XPATH,"//div[@srchresult='true']//div[contains(@class,'quoteSymbol')]"))   //div[contains(@class,'quoteSymbol')]
                #30/11/24 :
                EC.presence_of_element_located((By.XPATH,"//li[@data-test='srch-sym']//div[contains(@class,'quoteSymbol')]"))
            )
            self.yf_ticker=search_result.text
            search_box.clear()
            print(self.yf_ticker)
        except:
            print("Pas de résultat")
            self.rejected_isin=self.yf_ISIN
            YFISINScraperManager.driver.get(YF_URL_ROOT)
            

    def get_actifs_circulants(self):
        return self.yf_balance_sheet_scraper.get_balance_sheet_item_by_title('Actif à court terme')[0]
    
    def get_tresorerie(self):
        return self.yf_balance_sheet_scraper.get_balance_sheet_item_by_title('Trésorerie, quasi-espèces et investissements à court terme')[0]
    
    def get_actifs_intangibles(self):
        return self.yf_balance_sheet_scraper.get_balance_sheet_item_by_title('Clientèle')[0]+self.yf_balance_sheet_scraper.get_balance_sheet_item_by_title("Biens incorporels")[0]
    
    def get_actifs_totaux(self):
        return self.yf_balance_sheet_scraper.get_balance_sheet_item_by_title('Total des actifs')[0]
    
    def get_dette_totale(self):
        return self.yf_balance_sheet_scraper.get_balance_sheet_item_by_title('Passifs totaux')[0]
    
    def get_capitaux_propres(self):
        return self.yf_balance_sheet_scraper.get_balance_sheet_item_by_title('Participation minoritaire au total des fonds propres bruts')[0]
        
    def get_actifs_corporels_net(self):
        return self.yf_balance_sheet_scraper.get_balance_sheet_item_by_title('Actifs corporels nets')[0]
    
    def get_total_des_actifs(self):
        return self.yf_balance_sheet_scraper.get_balance_sheet_item_by_title('Total des actifs')[0]
    
    def get_participation_minoritaire(self):
        return self.yf_balance_sheet_scraper.get_balance_sheet_item_by_title('Participation minoritaire')[0]
    
    def get_valeur_comptable_tangible(self):
        return self.yf_balance_sheet_scraper.get_balance_sheet_item_by_title('Valeur comptable tangible')[0]
    
    def get_actifs_non_circulants(self):
        return self.yf_balance_sheet_scraper.get_balance_sheet_item_by_title('Total des actifs non circulants')[0]
    
    def get_immobilisations_incorporelles(self):
        return self.yf_balance_sheet_scraper.get_balance_sheet_item_by_title('Écarts d’acquisition et autres immobilisations incorporelles')[0]
    
    def __get_foncier(self):
        return self.yf_balance_sheet_scraper.get_balance_sheet_item_by_title('Foncier et améliorations')[0]
    
    def __get_constructions(self):
        return self.yf_balance_sheet_scraper.get_balance_sheet_item_by_title('Constructions et améliorations')[0]
    
    def get_estate(self):
        return self.__get_constructions()+self.__get_foncier()
    
    def get_cours(self):
        return self.yf_stat_scraper.get_stat_by_title("Cours")
    
    def get_actions(self):
        return self.yf_stat_scraper.get_stat_by_title("Actions en attente")
    
    def get_secteur(self):
        return self.yf_profile_scraper.get_profile_by_title("Secteur")
    
    def get_activite(self):
        return self.yf_profile_scraper.get_profile_by_title("Secteur d’activité")
    
    def get_website(self):
        return self.yf_profile_scraper.get_profile_by_title("Website")
    
    def get_nom(self):
        return self.yf_profile_scraper.get_profile_by_title("Nom")
    
    def get_rendement_dividende(self):
        return self.yf_stat_scraper.get_stat_by_title("Rendement en dividendes moyen")
