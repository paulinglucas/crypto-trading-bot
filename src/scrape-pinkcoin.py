import requests
from bs4 import BeautifulSoup

## arbitrary params, can be changes
COIN = 'pinkcoin'
START_DATE = '2016-02-27'
END_DATE = '2021-02-27'

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
    data_dict = {}
    for d in data:
        prices = d.find_all('td')
        data_dict[d.find('th').text] = {
            heads[1]: deal_with_na(prices[0].text.strip().replace("$", "").replace(",", "")),
            heads[2]: deal_with_na(prices[1].text.strip().replace("$", "").replace(",", "")),
            heads[3]: deal_with_na(prices[2].text.strip().replace("$", "").replace(",", "")),
            heads[4]: deal_with_na(prices[3].text.strip().replace("$", "").replace(",", ""))
        }

    return data_dict

def main():
    ## get url query from pinkcoin site
    URL = 'https://www.coingecko.com/en/coins/{}/historical_data/usd?end_date={}&start_date={}#panel'.format(COIN, END_DATE, START_DATE)
    page = requests.get(URL)

    ## HTML object from beautiful soup
    soup = BeautifulSoup(page.content, 'html.parser')

    ## extract table and place into dictionary
    data_dict = extract_table(soup)
    print(data_dict)



if __name__ == '__main__':
    main()
