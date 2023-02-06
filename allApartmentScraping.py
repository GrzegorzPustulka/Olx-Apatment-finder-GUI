from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import threading


@dataclass
class Ads:
    link: str
    price: float
    rent: float
    total: float


ads = []


def all_apartments_scraping(max_price, min_price, link, our_districts):
    thread_ads = []
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'lxml')
    ad = soup.select("a.css-rc5s2u")
    olx_ad = []
    for name in ad:
        if "otodom" not in name['href']:
            olx_ad.append("https://www.olx.pl" + name['href'])
        else:
            olx_ad.append(name['href'])

    # ad districts from olx 0-51
    olx_districts = soup.find_all("p", attrs={"data-testid": "location-date"})

    # ad price from olx 0-51
    olx_buffer_prices = soup.find_all("p", attrs={"data-testid": "ad-price"})

    # change prices from ad to friendly number
    text_prices = ''.join(i.text.replace(' ', '').replace(',', '.') for i in olx_buffer_prices)
    olx_prices = [float(x) for x in re.findall(r'\d*\.\d+|\d+', text_prices)]

    olx_rent = 0
    for i, district in enumerate(olx_districts):
        for name in our_districts:
            if name in district.text:
                if max_price >= olx_prices[i] >= min_price:
                    req = requests.get(olx_ad[i])
                    soup = BeautifulSoup(req.text, 'lxml')

                    if "olx.pl" in olx_ad[i]:
                        price_rent_buffer = soup.select('li.css-1r0si1e')
                        for tag in price_rent_buffer:
                            if "Czynsz" in tag.text:
                                text_prices = tag.text.replace(' ', '').replace(',', '.')
                                olx_rent = (int(re.findall(r'\d+', text_prices)[0]))
                    else:
                        olx_rent = 0
                    if max_price >= olx_prices[i] + olx_rent >= min_price:
                        ad = Ads(olx_ad[i], olx_prices[i], olx_rent, olx_prices[i] + olx_rent)
                        thread_ads.append(ad)
    ads.append(thread_ads)


def run_all_apartments(max_price, min_price, link, our_districts):
    threads = []
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'lxml')
    count_pages = int(soup.select('li[data-testid="pagination-list-item"]')[3].text)

    for i in range(count_pages):
        if i == 0:
            t = threading.Thread(target=all_apartments_scraping, args=(max_price, min_price, link, our_districts))
            threads.append(t)
            t.start()
        else:
            link = link + "?page=" + str(i + 1)
            t = threading.Thread(target=all_apartments_scraping, args=(max_price, min_price, link, our_districts))
            threads.append(t)
            t.start()

    for thread in threads:
        thread.join()

    final_results = []
    for ad in ads:
        final_results.extend(ad)

    df = pd.DataFrame(final_results)
    print(df)
    df.to_excel('AllApartment.xlsx')