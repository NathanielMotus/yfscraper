from selenium.webdriver.common.by import By
from yfscraper import yfutilities

CASHFLOW_LINE_TITLES=("Flux de trésorerie d’exploitation",
                           "Flux de trésorerie d’investissement")

CASHFLOW_HEADER_TITLE='Détails'

class YFCashflowScraper:
    # On ne récupère que les flux d'exploitation et d'investissement
    # chaque élément de la liste correspond à une ligne du tableau, sous la forme {poste : [valeur1, valeur2, etc.]}

    def __init__(self,cashflow_sheet_webdriver) -> None:
        self.cashflow_sheet={}
        self.cashflow_sheet_webdriver=cashflow_sheet_webdriver

    # récupère les lignes dont le titre est spécifié dans CASHFLOW_LINE_TITLES
    def get_cashflow_sheet(self):
        self.cashflow_sheet={}
        self.__get_header()
        for s in CASHFLOW_LINE_TITLES:
            self.__get_cashflow_sheet_line_by_title(s)

    # récupère le header, qui n'a pas le même format que les autres lignes
    def __get_header(self):
        try:
            header_root=self.cashflow_sheet_webdriver.find_element(By.XPATH,"//div[text()='"+CASHFLOW_HEADER_TITLE+"']").find_element(By.XPATH,"..")
            header_list=header_root.find_elements(By.TAG_NAME,'div')
            header_list_text=[]
            for i in range(1,len(header_list)):
                header_list_text.append(header_list[i].text)
            self.cashflow_sheet[header_list[0].text]=header_list_text
        except:
            self.cashflow_sheet[CASHFLOW_HEADER_TITLE]='NA'
    
    # trouve le WebElement qui contient les valeurs de la ligne
    def __find_cashflow_sheet_line_element_by_title(self,title):
        try:
            return self.cashflow_sheet_webdriver.find_element(By.XPATH,"//*[@title='"+title+"']").find_element(By.XPATH,"..").find_element(By.XPATH,"..")
        except:
            return None
    
    # récupère la ligne du bilan dont le titre est spécifié en paramètre
    def __get_cashflow_sheet_line_by_title(self,title):
        line=[]
        if self.__find_cashflow_sheet_line_element_by_title(title)!=None:
            line_elements=self.__find_cashflow_sheet_line_element_by_title(title).find_elements(By.XPATH,".//div[contains(@class,'column')]") # type: ignore
            for i in range(1,len(line_elements)):
                line.append(yfutilities.parse_financials_number(line_elements[i]))
            self.cashflow_sheet[line_elements[0].text]=line
    
    # renvoie l'item de la balance sheet désigné par son titre
    def get_cashflow_sheet_item_by_title(self,title)->list:
        try:
            return self.cashflow_sheet[title]
        except:
            return [0]

