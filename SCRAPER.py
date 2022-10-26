import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import sys
import requests
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

#SCRAPE 24HR CRYPTO PRICES FROM COINGECKO
def scrape_data():
    base_url = "https://www.coingecko.com/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    HEADERS = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; rv:87.0) Gecko/20100101 Firefox/12.0'   
    }

    #ITERATE FROM PAGE 1 OF COINGECKO
    for i in range(1,2):
        print('Processing page {0}'.format(i))
        params = {
            'page':i
        }

    #SCRAPE URL VIA COMMAND LINE

    #SCRAPE TABLE FROM COINGECKO 
    df = pd.DataFrame(pd.read_html(str(soup))[0])
    pd.read_html(str(soup))[0]

    #DELETE NULL COLUMNS 
    # df.drop(df.columns[[0,3]], axis=1, inplace=True)
    # df = df.drop(['Last 7 Days'], axis=1)
    # print(df.head(10))
    # df['Coin'].iloc[0] = 'BTC'
    # df['Coin'].iloc[1] = 'ETH'
   # df['Coin'].iloc[2] = 'USDT'
# df['Coin'].iloc[3] = 'USDC'
# df['Coin'].iloc[4] = 'BNB'
# df['Coin'].iloc[5] = 'XRP'
# df['Coin'].iloc[6] = 'ADA'
# df['Coin'].iloc[7] = 'BUSD'
# df['Coin'].iloc[8] = 'SOL'
# df['Coin'].iloc[9] = 'DOGE'
# print(df.head(10))

# df['1h'] = df['1h'].str[:-1].astype(float)
# df.iloc[0:5].plot(x='Coin', y='1h', style='o')
# plt.show()

# df['7d'] = df['7d'].str[:-1].astype(float)
# df.iloc[0:5].plot(x='Coin', y='7d', style='o')
# plt.show()

# df['24h'] = df['24h'].str[:-1].astype(float)
# df.iloc[0:5].plot(x='Coin', y='24h', style='o')
# plt.show()
    
    # 2nd dataset
    #COINS ANALYZED IN SCRAPING
    coin_list = ['BTC','ETH']

    #DEFINING THE DATAFRAME 
    main_df = pd.DataFrame()

    for coin in coin_list:
        coin_df = pd.DataFrame()
        df = pd.DataFrame(index=[0])


        #DEFINING START-DATE AND END-DATE 
        datetime_end = datetime(2021, 7, 2, 0, 0)
        datetime_check = datetime(2021, 7, 1, 0, 0)
        
        while len(df) > 0:
            if datetime_end == datetime_check:
                break

            datetime_start = datetime_end - relativedelta(hours = 12)

           #API USED FOR SCRAPING 
            url = 'https://production.api.coindesk.com/v2/price/values/'+ coin +'?start_date='+datetime_start.strftime("%Y-%m-%dT%H:%M") + '&end_date=' + datetime_end.strftime("%Y-%m-%dT%H:%M") + '&ohlc=true'

            #USING REQUEST TO FETCH DATA FROM API IN THE JSON FORMAT THEN STORE INTO DATAFRAME
            temp_data = requests.get(url).json()
            df = pd.DataFrame(temp_data['data']['entries'])
            #ADD COIN AND ITERATE BELOW 
            df.columns = ['Timestamp', 'Open', 'High', 'Low', 'Price']

           #HANDLE MISSING DATA 
            insert_ids_list = [np.nan]
            
             #ITERATE
            while len(insert_ids_list) > 0:
                timestamp_checking = np.array(df['Timestamp'][1:]) - np.array(df['Timestamp'][:-1])
                insert_ids_list = np.where(timestamp_checking!= 60000)[0]
                if len(insert_ids_list) > 0:
                    print(str(len(insert_ids_list)) + 'Processing Data')
                    insert_ids = insert_ids_list[0]
                    temp_df = df.iloc[insert_ids.repeat(int(timestamp_checking[insert_ids]/60000)-1)].reset_index(drop=True)
                    temp_df['Timestamp'] = [temp_df['Timestamp'][0] + i*60000 for i in range(1, len(temp_df)+1)]
                    df = df.loc[:insert_ids].append(temp_df).append(df.loc[insert_ids+1:]).reset_index(drop=True)
                    insert_ids_list = insert_ids_list[1:]
                    
             #ADDING DATETIME AND SYMBOL TO DATAFRAME
            df = df.drop(['Timestamp'], axis=1)
            df['Datetime'] = [datetime_end - relativedelta(minutes=len(df)-i) for i in range(0, len(df))]
            coin_df = df.append(coin_df)
            datetime_end = datetime_start
        
        coin_df['Coin'] = coin
        main_df = main_df.append(coin_df)
    
    #GENERATE DATAFRAME FOR FIRST FIVE ROWS OF BITCOIN AND ETHER
    main_df = main_df[['Datetime', 'Coin', 'Open', 'High', 'Low', 'Price']].reset_index(drop=True)
    print(main_df)
    
    #PLOT 24 HOUR BITCOIN PRICE
    main_df_BTC = main_df[['Coin','Price']]
    rslt_df_BTC = main_df_BTC[main_df_BTC['Coin'] == 'BTC']
    rslt_df_BTC[['Price']].plot(title='Bitcoin price over 1 day')
    plt.show()
    
    #PLOT 24 HOUR ETHEREUM PRICE
    main_df_ETH = main_df[['Coin','Price']]
    rslt_df_ETH = main_df_ETH[main_df_ETH['Coin'] == 'ETH']
    rslt_df_ETH[['Price']].plot(title='Ethereum price over 1 day')
    plt.show()
    
    rslt_df_ETH.rename(columns = {'Price':'ETH Price'}, inplace = True)
    rslt_df_BTC.rename(columns = {'Price':'BTC Price'}, inplace = True)
    
    # Dataset 3
    df = pd.read_csv ('ethervol.csv',usecols=['Date','Ethereum Volatility Index'])
    print(df)
    
    # PLOTTING VOLATILITY ON 10 DAY PERIOD LEADING TO 24 HOUR ANALYSIS FROM 2021 API 
    df['Date'].iloc[424] = '6/22'
    df['Date'].iloc[425] = '6/23'
    df['Date'].iloc[426] = '6/24'
    df['Date'].iloc[427] = '6/25'
    df['Date'].iloc[428] = '6/26'
    df['Date'].iloc[429] = '6/27'
    df['Date'].iloc[430] = '6/28'
    df['Date'].iloc[431] = '6/29'
    df['Date'].iloc[432] = '6/30'
    df['Date'].iloc[433] = '7/1'
    df['Date'].iloc[434] = '7/2'
    
    
    df.iloc[424:435].plot(x = 'Date')
    plt.show()
    
    #PLOTTING VOLATILITY ON 10 DAY PERIOD LEADING TO 24 HOUR ANALYSIS FROM 2022 WEBSCRAPED DATA 
    df['Date'].iloc[734] = '4/28'
    df['Date'].iloc[735] = '4/29'
    df['Date'].iloc[736] = '4/30'
    df['Date'].iloc[737] = '5/1'
    df['Date'].iloc[738] = '5/2'
    df['Date'].iloc[739] = '5/3'
    df['Date'].iloc[740] = '5/4'
    df['Date'].iloc[741] = '5/5'
    df['Date'].iloc[742] = '5/6'
    df['Date'].iloc[743] = '5/7'
    df['Date'].iloc[744] = '5/8'
    
    df.iloc[734:750].plot(x = 'Date')
    plt.show()
    

if __name__ == "__main__":
	scrape_data()