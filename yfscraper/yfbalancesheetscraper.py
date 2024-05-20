from selenium.webdriver.common.by import By
from yfscraper import yfutilities

BALANCE_SHEET_LINE_TITLES=("Trésorerie totale",
                           "Total des actifs à court terme",
                           "Investissements bruts en terrains, usines et équipements",
                           "Clientèle",
                           "Biens incorporels",
                           "Total des actifs non circulants",
                           "Total des actifs",
                           "Total des passifs à court terme",
                           "Total des passifs non à court terme",
                           "Passifs totaux",
                           "Total des capitaux propres")

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
            header_root=self.balance_sheet_webdriver.find_element(By.XPATH,"//span[text()='"+BALANCE_SHEET_HEADER_TITLE+"']").find_element(By.XPATH,"..").find_element(By.XPATH,"..")
            header_list=header_root.find_elements(By.TAG_NAME,'span')
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
            line_elements=self.__find_balance_sheet_line_element_by_title(title).find_elements(By.XPATH,'.//*[text()!=""]') # type: ignore
            for i in range(1,len(line_elements)):
                line.append(yfutilities.parse_financials_number(line_elements[i]))
            self.balance_sheet[line_elements[0].text]=line
    
    # renvoie l'item de la balance sheet désigné par son titre
    def get_balance_sheet_item_by_title(self,title)->list:
        try:
            return self.balance_sheet[title]
        except:
            return [0]

