import requests
from bs4 import BeautifulSoup
import csv

URL = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
table = soup.find('table', {'class': 'h4'})
trs = table.find_all('tr')[2:]
numbers = list()
for tr in trs:
	row = [td.text.replace('\n', '').replace('\xa0', '') for td in tr.find_all('td')]
	number = int(row[0][:4])
	numbers.append(number)
	if number == 9958:
		break

with open('number.csv', 'w', newline='') as numberFile:
    writer = csv.writer(numberFile)
    for number in numbers:
        writer.writerow([number])