import requests
from bs4 import BeautifulSoup
import csv

def getMainPower(stockNum): 
    urlBrokerTrading = "https://tw.stock.yahoo.com/quote/"+str(stockNum)+"/broker-trading"
    pageBrokerTrading = requests.get(urlBrokerTrading)

    soupBrokerTrading = BeautifulSoup(pageBrokerTrading.content, "html.parser")
    totalNum = soupBrokerTrading.find_all('span', {'class': 'Fz(16px) C($c-link-text) Mb(4px)'})
    stockName = soupBrokerTrading.find_all('h1', {'class': 'C($c-link-text) Fw(b) Fz(24px) Mend(8px)'})
    
    result = dict.fromkeys(['Num', 'Name', 'Value', 'Rate', 'Total',\
              'Buy1', 'Buy1_Ratio', 'Buy2', 'Buy2_Ratio', 'Buy3', 'Buy3_Ratio',\
              'Sell1', 'Sell1_Ratio', 'Sell2', 'Sell2_Ratio', 'Sell3', 'Sell3_Ratio'])
    
    result['Num'] = stockNum
    result['Name'] = stockName[0].text
    if totalNum[0].text == '-':
        return result
    result['Total'] = int(totalNum[0].text.replace(',',''))

    # many different display
    stockValue = soupBrokerTrading.find_all('span', {'class': 'Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)'})
    if len(stockValue) == 0:
        stockValue = soupBrokerTrading.find_all('span', {'class': 'Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)'})
    if len(stockValue) == 0:
        stockValue = soupBrokerTrading.find_all('span', {'class': 'Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)'})
    if len(stockValue) == 0:
        stockValue = soupBrokerTrading.find_all('span', {'class': 'Fz(32px) Fw(b) Lh(1) Mend(16px) C(#fff) Px(6px) Py(2px) Bdrs(4px) Bgc($c-trend-up)'})
    if len(stockValue) == 0:
        stockValue = soupBrokerTrading.find_all('span', {'class': 'Fz(32px) Fw(b) Lh(1) Mend(16px) C(#fff) Px(6px) Py(2px) Bdrs(4px) Bgc($c-trend-down)'})
    result['Value'] = stockValue[0].text

    stockRate = soupBrokerTrading.find_all('span', {'class': 'Jc(fe) Fz(20px) Lh(1.2) Fw(b) D(f) Ai(c) C($c-trend-up)'})
    if len(stockRate) == 0:
        stockRate = soupBrokerTrading.find_all('span', {'class': 'Jc(fe) Fz(20px) Lh(1.2) Fw(b) D(f) Ai(c) C($c-trend-down)'})
        if len(stockRate) == 0:
            stockRate = str(0)
        else:
            stockRate = "-" + str(stockRate[0].text)
    else:        
        stockRate = "+" + str(stockRate[0].text)
    result['Rate'] = stockRate * 100

    divsBuy = soupBrokerTrading.find('div', {'class': 'W(50%) W(100%)--mobile Mb(20px)--mobile'})
    buyName = divsBuy.find_all('span', {'class': 'W(34%) Ta(s)'})
    buyNum = divsBuy.find_all('span', {'class': 'Jc(fe) W(22%) Ta(e) Fw(b) D(f) Ai(c) C($c-trend-up)'})
    divSold = soupBrokerTrading.find('div', {'class': 'W(50%) W(100%)--mobile'})
    soldName = divSold.find_all('span', {'class': 'W(34%) Ta(s)'})
    soldNum = divSold.find_all('span', {'class': 'Jc(fe) W(22%) Ta(e) Fw(b) D(f) Ai(c) C($c-trend-down)'})
    
    # get company name and buying number
    for i in range(0, min(3, len(buyNum))):
        if i == 0:
            result['Buy1'] = buyName[i+1].text
            result['Buy1_Ratio'] = int(buyNum[i].text.replace(',',''))/result['Total']
        elif i == 1:
            result['Buy2'] = buyName[i+1].text
            result['Buy2_Ratio'] = int(buyNum[i].text.replace(',',''))/result['Total']
        else:
            result['Buy3'] = buyName[i+1].text
            result['Buy3_Ratio'] = int(buyNum[i].text.replace(',',''))/result['Total']
    # get company name and selling number
    for i in range(0, min(3, len(soldNum))):
        if i == 0:
            result['Sell1'] = soldName[i+1].text
            result['Sell1_Ratio'] = int(soldNum[i].text.replace(',',''))/result['Total']
        elif i == 1:
            result['Sell2'] = soldName[i+1].text
            result['Sell2_Ratio'] = int(soldNum[i].text.replace(',',''))/result['Total']
        else:
            result['Sell3'] = soldName[i+1].text
            result['Sell3_Ratio'] = int(soldNum[i].text.replace(',',''))/result['Total']
    print(stockNum)
    return result

results = []
with open('number.csv', newline='') as csvfile:
    rows = csv.reader(csvfile)
    i = 0
    for r in rows:
        i = i + 1
        #if i == 10:
        #    break       
        results.append(getMainPower(int(r[0])))

with open('output.csv', 'w', newline='') as csvfile:
    labels = ['Num', 'Name', 'Value', 'Rate', 'Total',\
              'Buy1', 'Buy1_Ratio', 'Buy2', 'Buy2_Ratio', 'Buy3', 'Buy3_Ratio',\
              'Sell1', 'Sell1_Ratio', 'Sell2', 'Sell2_Ratio', 'Sell3', 'Sell3_Ratio']
    writer = csv.DictWriter(csvfile, fieldnames = labels)
    writer.writeheader()
    for r in results:
        writer.writerow(r)
