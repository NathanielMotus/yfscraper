from yfscraper.yfisinscrapermanager import YFISINScraperManager

class YFAnalyzer:

    def __init__(self,yf_scraper_manager:YFISINScraperManager):
        self.yf_scraper_manager=yf_scraper_manager

    def __get_VANTPA(self):
        if self.yf_scraper_manager.get_actions()!=0:
            return float(format(self.yf_scraper_manager.get_valeur_comptable_tangible()/self.yf_scraper_manager.get_actions(),'.2f'))
        else:
            return 0
        
    def __get_ratio_cours_VANTPA(self):
        if self.__get_VANTPA()!=0:
            return float(format(self.yf_scraper_manager.get_cours()/float(self.__get_VANTPA()),'.2f'))
        else:
            return 0
    
    def __get_VANNPA(self):
        if self.yf_scraper_manager.get_actions()!=0:
            return float(format((self.yf_scraper_manager.get_valeur_comptable_tangible()-(self.yf_scraper_manager.get_actifs_non_circulants()-self.yf_scraper_manager.get_immobilisations_incorporelles()))/self.yf_scraper_manager.get_actions(),'.2f'))
        else:
            return 0
        
    def __get_ratio_cours_VANNPA(self):
        if self.__get_VANNPA()!=0:
            return float(format(self.yf_scraper_manager.get_cours()/float(self.__get_VANNPA()),'.2f'))
        else:
            return 0
        
    def __get_solvabilite(self):
        try:
            return float(format(((self.yf_scraper_manager.get_capitaux_propres()-self.yf_scraper_manager.get_participation_minoritaire())/(self.yf_scraper_manager.get_actifs_totaux()-self.yf_scraper_manager.get_tresorerie())),'.2f'))
        except:
            return 0
        
    def __get_rendement_moyen_dividendes(self):
        try:
            return float(format((self.yf_scraper_manager.get_rendement_dividende()/self.yf_scraper_manager.get_cours()),'.2f'))
        except:
            return 0
        
    def __get_VANEPA(self):
        if self.yf_scraper_manager.get_actions()!=0:
            return float(format((self.yf_scraper_manager.get_valeur_comptable_tangible()-(self.yf_scraper_manager.get_actifs_non_circulants()-self.yf_scraper_manager.get_immobilisations_incorporelles())+0.8*self.yf_scraper_manager.get_estate())/self.yf_scraper_manager.get_actions(),'.2f'))
        else:
            return 0
        
    def __get_ratio_cours_VANEPA(self):
        if self.__get_VANEPA()!=0:
            return float(format(self.yf_scraper_manager.get_cours()/float(self.__get_VANEPA()),'.2f'))
        else:
            return 0
        
    def __get_FCFPA_actualises(self):
        #renvoie les cash flow moyens actualisés à 12%
        try:
            return float(format(self.yf_scraper_manager.get_fcf_moyens()/self.yf_scraper_manager.get_actions()*1.12/.12,'.2f'))
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
                 self.__get_ratio_cours_VANEPA(),
                 self.__get_solvabilite(),
                 self.__get_rendement_moyen_dividendes(),
                 self.__get_FCFPA_actualises()])
