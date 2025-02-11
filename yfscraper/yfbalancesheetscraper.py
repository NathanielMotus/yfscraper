from selenium.webdriver.common.by import By
from yfscraper import yfutilities

#historique
#BALANCE_SHEET_LINE_TITLES=("Trésorerie totale",
#                           "Total des actifs à court terme",
#                           "Investissements bruts en terrains, usines et équipements",
#                           "Clientèle",
#                           "Biens incorporels",
#                           "Total des actifs non circulants",
#                           "Total des actifs",
#                           "Total des passifs à court terme",
#                           "Total des passifs non à court terme",
#                           "Passifs totaux",
#                           "Total des capitaux propres")
#30/11/24 :
#BALANCE_SHEET_LINE_TITLES=("Total des actifs",
#                           "Actif à court terme",
#                           "Trésorerie",
#                           "Participation minoritaire au total des fonds propres bruts",#capitaux propres
#                           "Participation minoritaire",
#                           "Actifs corporels nets")

#11/02/25
#A revoir :
#VANT="Valeur comptable tangible"
#VANN="Valeur comptable tangible"-"Total des actifs non circulants"+"Écarts d’acquisition et autres immobilisations incorporelles"
#VANE=VANN+"Autres propriétés"

BALANCE_SHEET_LINE_TITLES=("Valeur comptable tangible",
                           "Total des actifs",
                           "Total des actifs non circulants",
                           "Trésorerie, quasi-espèces et investissements à court terme",
                           "Écarts d’acquisition et autres immobilisations incorporelles",
                           "Autres propriétés",
                           "Participation minoritaire au total des fonds propres bruts",
                           "Participation minoritaire")

BALANCE_SHEET_HEADER_TITLE='Détails'

class YFBalanceSheetScraper:
    # La balance-sheet est un dictionnaire de listes
    # chaque élément de la liste correspond à une ligne du tableau, sous la forme {poste : [valeur1, valeur2, etc.]}

    def __init__(self,balance_sheet_webdriver) -> None:
        self.balance_sheet={}
        self.balance_sheet_webdriver=balance_sheet_webdriver

    # récupère les lignes dont le titre est spécifié dans BALANCE_SHEET_LINE_TITLES
    def get_balance_sheet(self):
        self.balance_sheet={}
        self.__get_header()
        for s in BALANCE_SHEET_LINE_TITLES:
            self.__get_balance_sheet_line_by_title(s)

    # récupère le header, qui n'a pas le même format que les autres lignes
    def __get_header(self):
        try:
            #historique
            #header_root=self.balance_sheet_webdriver.find_element(By.XPATH,"//span[text()='"+BALANCE_SHEET_HEADER_TITLE+"']").find_element(By.XPATH,"..").find_element(By.XPATH,"..")
            #header_list=header_root.find_elements(By.TAG_NAME,'span')
            #30/11/24 :
            header_root=self.balance_sheet_webdriver.find_element(By.XPATH,"//div[text()='"+BALANCE_SHEET_HEADER_TITLE+"']").find_element(By.XPATH,"..")
            header_list=header_root.find_elements(By.TAG_NAME,'div')
            header_list_text=[]
            for i in range(1,len(header_list)):
                header_list_text.append(header_list[i].text)
            self.balance_sheet[header_list[0].text]=header_list_text
        except:
            self.balance_sheet[BALANCE_SHEET_HEADER_TITLE]='NA'
    
    # trouve le WebElement qui contient les valeurs de la ligne
    def __find_balance_sheet_line_element_by_title(self,title):
        try:
            return self.balance_sheet_webdriver.find_element(By.XPATH,"//*[@title='"+title+"']").find_element(By.XPATH,"..").find_element(By.XPATH,"..")
        except:
            return None
    
    # récupère la ligne du bilan dont le titre est spécifié en paramètre
    def __get_balance_sheet_line_by_title(self,title):
        line=[]
        if self.__find_balance_sheet_line_element_by_title(title)!=None:
            line_elements=self.__find_balance_sheet_line_element_by_title(title).find_elements(By.XPATH,".//div[contains(@class,'column')]") # type: ignore
            for i in range(1,len(line_elements)):
                line.append(yfutilities.parse_financials_number(line_elements[i]))
            self.balance_sheet[line_elements[0].text]=line
    
    # renvoie l'item de la balance sheet désigné par son titre
    def get_balance_sheet_item_by_title(self,title)->list:
        try:
            return self.balance_sheet[title]
        except:
            return [0]

