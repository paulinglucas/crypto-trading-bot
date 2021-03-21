import requests, sys
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


## arbitrary params, can be changed
COIN = 'pinkcoin'
START_DATE = '2016-02-27'
today = datetime.now()
END_DATE = datetime.strftime(today, '%Y-%m-%d')

## some columns have null values, fill with 'N/A'
def deal_with_na(price_pt):
    if 'N/A' in price_pt:
        return 'N/A'
    else:
        return float(price_pt)

## extract table of historical data from coin and return dictionary of parsed data
def extract_table(soup):
    ## grab header titles
    hist_head = soup.find('thead')
    headers = hist_head.find_all('th')
    heads = []
    for h in headers:
        heads.append(h.text)

    ## get body data
    hist_body = soup.find('tbody')
    data = hist_body.find_all('tr')

    ## begin filling dictionary with data
    dates = []
    prices = []
    for d in data:
        curr_data = d.find_all('td')
        dates.append(d.find('th').text)
        cap =   deal_with_na(curr_data[0].text.strip().replace("$", "").replace(",", ""))
        vol =   deal_with_na(curr_data[1].text.strip().replace("$", "").replace(",", ""))
        open =  deal_with_na(curr_data[2].text.strip().replace("$", "").replace(",", ""))
        close = deal_with_na(curr_data[3].text.strip().replace("$", "").replace(",", ""))
        prices.append([cap, vol, open, close])

    return dates, prices

## plot data frame onto graph
def visualize_data(df):
    ## remove all null closing values, should just disclude current day
    df = df[df.Close != 'N/A']

    ## plot
    sns.regplot(x = "Market_Cap", y="Volume", data=df, fit_reg = False, scatter_kws={"alpha": 0.2})
    plt.show()

    return 0

def main():
    # # make sure variables are inserted
    # if len(sys.argv) != 3:
    #     print("USAGE: python3 scrape-pinkcoin.py [COLUMN 1] [COLUMN 2]")
    #     print("Columns to choose from:")
    #     print("     Market_Cap")
    #     print("     Volume")
    #     print("     Open")
    #     print("     Close")
    #     sys.exit(0)

    ## get url query from pinkcoin site
    URL = 'https://www.coingecko.com/en/coins/{}/historical_data/usd?end_date={}&start_date={}#panel'.format(COIN, END_DATE, START_DATE)
    page = requests.get(URL)

    ## HTML object from beautiful soup
    soup = BeautifulSoup(page.content, 'html.parser')

    ## extract table and place into dictionary
    dates, prices = extract_table(soup)

    ## create data frame from scraped data
    df = pd.DataFrame(prices, index=dates, columns=['Market_Cap', 'Volume', 'Open', 'Close'])

    df.to_excel('../excel_sheets/coin_data.xlsx')
    print(df)

    ## plot onto graph
    visualize_data(df) #, sys.argv[1], sys.argv[2])



if __name__ == '__main__':
    main()
