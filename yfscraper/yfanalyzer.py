from yfscraper.yfisinscrapermanager import YFISINScraperManager

class YFAnalyzer:

    def __init__(self,yf_scraper_manager:YFISINScraperManager):
        self.yf_scraper_manager=yf_scraper_manager

    def __get_VANTPA(self):
        if self.yf_scraper_manager.get_actions()!=0:
            return float(format((self.yf_scraper_manager.get_actifs_totaux()-self.yf_scraper_manager.get_actifs_intangibles())/self.yf_scraper_manager.get_actions(),'.2f'))
        else:
            return 0
        
    def __get_ratio_cours_VANTPA(self):
        if self.__get_VANTPA()!=0:
            return float(format(self.yf_scraper_manager.get_cours()/float(self.__get_VANTPA()),'.2f'))
        else:
            return 0
    
    def __get_VANNPA(self):
        if self.yf_scraper_manager.get_actions()!=0:
            return float(format((self.yf_scraper_manager.get_actifs_circulants()-self.yf_scraper_manager.get_dette_totale())/self.yf_scraper_manager.get_actions(),'.2f'))
        else:
            return 0
        
    def __get_ratio_cours_VANNPA(self):
        if self.__get_VANNPA()!=0:
            return float(format(self.yf_scraper_manager.get_cours()/float(self.__get_VANNPA()),'.2f'))
        else:
            return 0
        
    def __get_solvabilite(self):
        try:
            return float(format((self.yf_scraper_manager.get_capitaux_propres()/(self.yf_scraper_manager.get_actifs_totaux()-self.yf_scraper_manager.get_tresorerie_totale())),'.2f'))
        except:
            return 0
        
    def get_analyze_line(self):
        return ([self.yf_scraper_manager.get_secteur(),
                 self.yf_scraper_manager.get_activite(),
                 self.yf_scraper_manager.get_website(),
                 self.yf_scraper_manager.get_nom(),
                 self.yf_scraper_manager.get_cours(),
                 self.__get_VANTPA(),
                 self.__get_ratio_cours_VANTPA(),
                 self.__get_ratio_cours_VANNPA(),
                 self.__get_solvabilite(),
                 self.yf_scraper_manager.get_rendement_dividende()])
