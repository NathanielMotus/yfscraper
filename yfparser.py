from yfscraper.yfisinscrapermanager import YFISINScraperManager
from yfscraper.yfanalyzer import YFAnalyzer
import csv

TICKERS_FILENAME='tickers.csv'

TICKERS=[]
with open(TICKERS_FILENAME,'r') as csvfile:
    reader=csv.reader(csvfile,delimiter=";")
    for row in reader:
        TICKERS.append(row[0])

with open('analysis.csv','w',newline='') as csvfile:
    filewriter=csv.writer(csvfile,delimiter=";")
    filewriter.writerow(['Ticker',
                         'Secteur',
                         'Activité',
                         'Website',
                         'Nom',
                         'Cours',
                         'VANTPA',
                         'Cours/VANTPA',
                         'Cours/VANNPA',
                         'Solvabilité',
                         'Rendement dividende %'])
    for t in TICKERS:
        manager=YFISINScraperManager(t)
        if manager.yf_ticker!='':
            line=YFAnalyzer(manager).get_analyze_line()
            line.insert(0,t)
            filewriter.writerow(line)
            print(line)

