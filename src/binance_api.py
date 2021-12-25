from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pandas as pd


def get_historical_data(api_key, 
                        api_secret, 
                        coin_pair, 
                        tweet_time,
                        min_interval, 
                        kline_type,
                        ):
    #connect to the api
    client = Client(api_key, api_secret)

    #get all the trading pairs and their latest prices
    prices = client.get_all_tickers()
    prices_df = pd.DataFrame(prices)

    klines = client.get_historical_klines(
                    symbol= coin_pair,
                    interval= min_interval,
                    start_str = tweet_time,
                    limit = 1000, #max is 1000 & default is 500
                    # klines_type = kline_type
                    )

    print(len(klines))
    
    #convert returned OHLCV values to pandas dataframe
    df_hist = pd.DataFrame(klines, 
                     columns = [
                    'open_time', 'open_price','high_price',
                    'low_price','close_price','volume',
                    'close_time','quote_asses_volume','no_of_trades',
                    'taker_buy_base_asset_volume','taker_buy_quote_asset_volume','ignore'
                ])

    #change datatype to datetime
    df_hist['open_time'] =  pd.to_datetime(df_hist['open_time'], unit='ms')
    df_hist['close_time'] =  pd.to_datetime(df_hist['close_time'], unit='ms')

    print(df_hist.info())

    return df_hist