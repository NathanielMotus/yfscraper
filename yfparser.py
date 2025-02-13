from yfscraper.yfisinscrapermanager import YFISINScraperManager
from yfscraper.yfanalyzer import YFAnalyzer
import csv

ISIN_FILENAME='isin suivis.csv'
DONE_FILENAME='done.csv'
reject_counter=1

ISIN=[]
with open(ISIN_FILENAME,'r') as csvfile:
    reader=csv.reader(csvfile,delimiter=";")
    for row in reader:
        ISIN.append(row[0])

with open('analysis.csv','a',newline='') as csvfile:
    filewriter=csv.writer(csvfile,delimiter=";")
    filewriter.writerow(['ISIN',
                         'Ticker',
                         'Secteur',
                         'Activité',
                         'Website',
                         'Nom',
                         'Cours',
                         'VANTPA',
                         'Cours/VANTPA',
                         'Cours/VANNPA',
                         'Cours/VANEPA',
                         'Solvabilité',
                         'Rendement dividende %'])
    
for t in ISIN:
    manager=YFISINScraperManager(t,reject_counter)
    if reject_counter==0:
        reject_counter=1
    if manager.yf_ticker!='':
        try:
            line=YFAnalyzer(manager).get_analyze_line()
            line.insert(0,manager.yf_ticker)
            line.insert(0,t)
            with open('analysis.csv','a',newline='') as csvfile:
                filewriter=csv.writer(csvfile,delimiter=";")
                filewriter.writerow(line)
            with open(DONE_FILENAME,'a',newline='') as done_csvfile:
                done_csvfile.write(t+"\n")
            print(line)
        except:
            ISIN.append(t)
            reject_counter=0
    else :
        ISIN.append(manager.rejected_isin)
        #remet à 0 le compteur tous les x
        reject_counter=(reject_counter+1)%20

