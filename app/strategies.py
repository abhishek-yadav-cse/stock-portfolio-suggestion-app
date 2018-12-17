#get history information of an stock
from yahoo_finance import Share
from iexfinance.stocks import Stock
from iexfinance.stocks import get_historical_data
from collections import defaultdict, OrderedDict
import datetime
import pandas as pd
import pandas_datareader.data as pdr
import json
import numpy as np, numpy.random


# get history_stock_info for stock_name

def get_historical_info_pandas(stock_short):
    end = datetime.datetime.now().date()
    # get the date of 7 days ago
    date_gap = datetime.timedelta(days=5)
    print ("1")
    print ("end ", end)
    print ("date_gap", date_gap)
    start = end - date_gap
    print ("start", start)
    # history for 7 days
   # stock_history_frame = pdr.DataReader(stock_short,'google',str(date_time_sevendays_ago),str(date_time_current))

    #df=pd.DataFrame(stock_history_frame)
    df= get_historical_data(stock_short, start, end, output_format= 'pandas' )
    print ("df", df)
    close_df=df
    print ("2")
    #"can edit"
    print ("close df", type(close_df))
    tk= df.values.tolist()
    print ("tk ", tk)

    close_price_dic=close_df.to_dict()
    print ("close price", close_price_dic)
    print ("3")
    stock_history= []
    # for ts in tk:
    # print ("blah ",close_price_dic['open']['2018-12-10 00:00:00'])
    #
    # stock_history = [(ts.strftime("%Y-%m-%d"), close_price_dic[ts]) for ts in tk]
    # print ("stock history", stock_history)
    index=0
   # list_items= ['open', 'high', 'low', 'close', 'volume']
    list_items= ['close']
    for items in list_items:
        for key, value in close_price_dic[items].items():
            stock_history.append((key, tk[index][0]))
            index +=1
        print (stock_history)
        index=0

    return stock_history


def get_historical_info(stock_short):
    stock_share= Stock(stock_short)
    date_time_current= datetime.datetime.now().date()
    #get the date of 7 days ago
    date_gap=datetime.timedelta(days=7)
    date_time_sevendays_ago = date_time_current-date_gap
    #history for 7 days
    stock_history = stock_share.get_historical(str(date_time_sevendays_ago), str(date_time_current))
    return stock_history

# get the current info of the latest stock info from yahoo_finance
def get_current_stock_info(stock_short):
   # print ("stock short", stock_short)
    stock_share = Stock(stock_short)
  #  print ("yahoo finance ", Share(stock_short).get_trade_datetime())
    stock_current_info={}
    stock_current_info['stock_short']=stock_short
    stock_latest_price=stock_share.get_price()
    stock_current_info['stock_latest_price']=stock_latest_price
    # stock_trade_datetime = stock_share.get_trade_datetime()
    # stock_current_info['stock_trade_datetime'] = stock_trade_datetime
    stock_exchange = stock_share.get_primary_exchange()
  #  print ("stock exchange", stock_exchange)
    stock_current_info['stock_exchange'] = stock_exchange
    stock_company_name = stock_share.get_company_name()
    stock_current_info['stock_company_name'] = stock_company_name
  #  print ("final info ", stock_current_info)
    return stock_current_info


# get all the stock list and according percentage for the selected strategies
def get_stock_list_all(strategy_list):
    print ("in in stock list all")
    stock_percent_list={}
    if(len(strategy_list)==1):
        stock_percent_list=get_stock_list(strategy_list[0],1)

    else:
        for strategy in strategy_list:
            stock_percent_list.update(get_stock_list(strategy,0.5))
    return stock_percent_list


stock_info = {
        'Ethical': ('AAPL', 'ADBE', 'NUE', 'GILD', 'GOOGL'),
        'Growth': ('BIIB', 'AKRX', 'IPGP', 'PSXP', 'NFLX'),
        'Index': ('VTI', 'IXUS', 'ILTB', 'VIS', 'KRE', 'VEU'),
        'Quality': ('QUAL', 'SPHQ', 'DGRW', 'QDF'),
        'Value': ('AAON', 'CTB', 'JNJ', 'GRUB', 'TTGT')
    }
#get the stock list and according percentage for one selected strategy, and the allotment is divided equally
def get_stock_list(strategy,strategy_ratio):

    stocks = stock_info[strategy]
    print ("in in get stock list")
    print ("stocks all", stocks)
    for s in stocks:
        print("stock", s)
        print ("stocks ", Stock(s).get_quote().get('change'))

    change_name = [(float(Stock(name).get_quote().get('change')), name) for name in stocks]
    change_name.sort(key=lambda x: -x[0])
    print("avni 1")
    top_stocks = [change_name[i][1] for i in range(3)] #select the top3 stocks
    #get random ratio of stock
    random_ratio = np.mean(np.random.dirichlet(np.ones(3), 10), axis=0).tolist()
    # the stocks_list for the selected strategies
    stock_percent_list={}
    for i in range(0,len(top_stocks)):
        stock_percent_list[stocks[i]]= random_ratio[i] * strategy_ratio

    return stock_percent_list


def get_strategy_stock_info(stock_list,investment):

    stock_strategy_invest_info={}

    for stock_short in stock_list:
        stock_current_info=get_current_stock_info(stock_short)
       # print ("stock current", stock_current_info)
        holding_ratio=stock_list[stock_short]
        stock_current_info['holding_ratio']=float("{0:.4f}".format(holding_ratio))
        stock_current_info['holding_value'] = float("{0:.2f}".format(holding_ratio*investment))
        stock_strategy_invest_info[stock_short]=stock_current_info

    return stock_strategy_invest_info


def get_historical_strategy_stock_value(stock_list,investment):
    stock_historical_values= defaultdict(float)
    ordered_date = []
    for stock_short in stock_list:

        historical_info=get_historical_info_pandas(stock_short)

        print("historical info ",historical_info)
        if not ordered_date:
            ordered_date = [itm[0] for itm in historical_info]
        holding_ratio = stock_list[stock_short]
        point_price=historical_info[0][1]
        print (len(historical_info))
        for i in range(len(historical_info)):
            stock_historical_values[historical_info[i][0]]+= historical_info[i][1]/point_price*investment*holding_ratio
    result = []
    for date in ordered_date:
        dict_json = {}
        dict_json['date'] = date
        dict_json['value'] = float("{0:.2f}".format(stock_historical_values[date]))
        result.append(dict_json)
    #json_str = json.dumps(dict_json)
    # print(len(result))
    return result
