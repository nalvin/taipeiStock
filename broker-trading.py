import requests
from bs4 import BeautifulSoup
import csv

def getMainPower(stockNum): 
    urlBrokerTrading = "https://tw.stock.yahoo.com/quote/"+str(stockNum)+"/broker-trading"
    pageBrokerTrading = requests.get(urlBrokerTrading)

    soupBrokerTrading = BeautifulSoup(pageBrokerTrading.content, "html.parser")
    divsBrokerTrading = soupBrokerTrading.find('div', {'class': 'W(50%) W(100%)--mobile Mb(20px)--mobile'})
    totalNum = soupBrokerTrading.find_all('span', {'class': 'Fz(16px) C($c-link-text) Mb(4px)'})
    if totalNum[0].text == '-':
        return [[], [], []]
    spansBrokerTradingName = divsBrokerTrading.find_all('span', {'class': 'W(34%) Ta(s)'})
    spansBrokerTradingNum = divsBrokerTrading.find_all('span', {'class': 'Jc(fe) W(22%) Ta(e) Fw(b) D(f) Ai(c) C($c-trend-up)'})
    names = list()
    numbers = list()
    # get company name and buying number
    for i in range(0, len(spansBrokerTradingNum)):
        names.append(spansBrokerTradingName[i+1].text)
        numbers.append(int(spansBrokerTradingNum[i].text.replace(',','')))
    return [int(totalNum[0].text.replace(',','')), names, numbers]

results = []
stockNums = []
with open('number.csv', newline='') as csvfile:
    rows = csv.reader(csvfile)
    for r in rows:
        results.append(getMainPower(int(r[0])))
        stockNums.append(int(r[0]))

with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for num in range(0, len(stockNums)):
        row = [stockNums[num]]
        for i in range(0, min(5, len(results[num][1]))):
            row.append(results[num][1][i])
            row.append(results[num][2][i]/results[num][0])
        writer.writerow(row)