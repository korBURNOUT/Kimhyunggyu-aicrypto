import time
import requests
import pandas as pd
import datetime


print('price,quantity,type,timestamp')



i=0
while(1):
    
   

    book = {}
    response = requests.get ('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5')
    book = response.json()



    data = book['data']

    bids = (pd.DataFrame(data['bids'])).apply(pd.to_numeric,errors='ignore')
    bids.sort_values('price', ascending=False, inplace=True)
    bids = bids.reset_index(); del bids['index']
    bids['type'] = 0
    
    asks = (pd.DataFrame(data['asks'])).apply(pd.to_numeric,errors='ignore')
    asks.sort_values('price', ascending=True, inplace=True)
    asks['type'] = 1 

    #print (bids)
    #print ("\n")
    #print (asks)

    
    df = pd.concat([bids,asks])
    
    timestamp = datetime.datetime.now()
    req_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    df['quantity'] = df['quantity'].round(decimals=4)
    df['timestamp'] = req_timestamp
    
    print (df)
    
    print ("\n")







    timestamp2 = timestamp.strftime('%Y-%m-%d')
    name = "%s-bithumb-btc-orderbook"% (timestamp2)
    #print(name)



    if(i==0):
        df.to_csv("./%s.csv"% (name), index=False, header=['price','quantity','type','timestamp'], mode = 'a')

    else:
        df.to_csv("./%s.csv"% (name), index=False, header=False, mode = 'a')
              



    #should_write_header = os.path.exists(fn)
    #if should_write_header == False:
    #    df.to_csv(fn, index=False, header=True, mode = 'a')
    #else:
    #    df.to_csv(fn, index=False, header=False, mode = 'a')

    time.sleep(1.0)

    i+=1
