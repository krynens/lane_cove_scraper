import os
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"

from bs4 import BeautifulSoup
from datetime import datetime
import requests
import scraperwiki

today = datetime.today()

url = 'http://ecouncil.lanecove.nsw.gov.au/trim/advertisedDAs.aspx'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'lxml')

table = soup.find('div', class_='bodypanel')
rows = table.find_all('table', class_='tabular-data table')

for row in rows:
    record = {}
    address = row.find('td', class_='current-development-applications')
    suburb = address.find_previous('h2').text.strip().title()
    record['address'] = f'{address.text.strip()}, {suburb}'
    record['date_scraped'] = today.strftime("%Y-%m-%d")
    record['description'] = row.find('td', colspan='2').text.strip()
    record['council_reference'] = row.find('a', style='text-decoration:underline; color:blue').text
    record['info_url'] = str(row.find(
        'a', style='text-decoration:underline; color:blue')).split('"')[1]
    record['on_notice_from'] = row.find_all('td')[13].text.strip().split(' Expiry: ')[0]
    record['on_notice_to'] = row.find_all('td')[13].text.strip().split(' Expiry: ')[1]

    scraperwiki.sqlite.save(
        unique_keys=['council_reference'], data=record, table_name="data")
