#from _typeshed import ReadableBuffer
from flask import Flask, render_template,request
from patterns import patterns
import yfinance as yf
import os
import pandas as pd
import numpy as np
import talib
import csv
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from nsepy import get_history
import pandas_ta as ta



app = Flask(__name__,static_url_path='/static')

@app.route("/")
def index():
    pattern=request.args.get('pattern',None)
    stocks={}

    #with open('datasets/data.csv') as f:
    #    for row in csv.reader(f):
    #        print(row[1])
    #        print(row[2])
    #        a=row[1]
    #        stocks[row[1]]={'company':a}
    with open('datasets/data.csv') as f:
        
        companies = f.read().splitlines()
        #print("companies :")
        print(companies)
        for company in companies:
            symbol = company.split(',')[0]
            stocks[symbol]={'company':symbol}
    
    print(stocks)
    if pattern:
        datafiles=os.listdir('datasets/daily')
        print(datafiles)
        #print(datafiles)
        for filename in datafiles:
           #filename.seek(0)
           #df= pd.read_csv('datasets/daily/TJX.csv')            #hardcoding script
           df= pd.read_csv('datasets/daily/{}'.format(filename),encoding= 'unicode_escape')            #hardcoding script
           
           #fig = go.Figure(data=[go.Candlestick(x=df['Date'],
            #    open=df['Open'],
             #   high=df['High'],
              #  low=df['Low'],
               # close=df['Close'])])

           #print(df)

           pattern_function=getattr(talib,pattern)
           symbol=filename.split('.')[0]
           print('symbols :: ')
           print(symbol)
           try:
                result=pattern_function(df['Open'],df['High'],df['Low'],df['Close'])
                last=result.tail(1).values[0]
                print(last)
                #symbol1=symbol+'.NS'
                
                if last>0:
                    stocks[symbol][pattern]='bullish'
                    print('bullish')
                
                elif last<0:
                    stocks[symbol][pattern]='bearish'
                    print('bullish')
                else:
                    stocks[symbol][pattern]=None
           
           except:
             pass
           


    return render_template('index.html',patterns=patterns,stocks=stocks,current_pattern=pattern)


@app.route("/snapshot")
def snapshot():
    
    with open('datasets/data.csv') as f:
        
        companies = f.read().splitlines()
        #print("companies :")
        print(companies)
        for company in companies:
            symbol = company.split(',')[0]
            print(symbol)
            #df=yf.download(symbol,start="2021-10-01",end="2021-12-16")
            df=get_history(symbol,
                   start=date(2021,10,30),
                   end=date(2022,2,1))
            
            df.ta.sma(close='close', length=5, append=True)
            df.ta.rsi(close='close', length=14, append=True)
            df.to_csv('datasets/daily/{}'.format(symbol))
            idf= pd.read_csv('datasets/daily/{}'.format(symbol),encoding= 'unicode_escape')            #hardcoding script
            idf=idf.tail(20)
            fig = go.Figure(data=[go.Candlestick(x=idf['Date'],
                open=idf['Open'],
                high=idf['High'],
                low=idf['Low'],
                close=idf['Close'])])
            #fig.show()
            layout = go.Layout(
            plot_bgcolor='#efefef',
            # Font Families
            font_family='Monospace',
            font_color='#000000',
            font_size=20,
            xaxis=dict(
                rangeslider=dict(
                    visible=False
                ))
            )
            fig.update_layout(layout)
            """
            fig.add_trace(
                go.Scatter(
                    x=idf.index,
                    y=idf['SMA_5'],
                    line=dict(color='#ff9900', width=2),
                    name='SMA_5'
                )
            )
            """
            fig.write_image('static/{}.jpg'.format(symbol))

        """
        datafiles=os.walk('datasets/daily')
        for filename in datafiles:
            print(filename)
            df= pd.read_csv('datasets/daily/{}'.format(filename),encoding= 'unicode_escape')            #hardcoding script
            df=df.tail(10)
            print(df.columns.tolist())
            
            fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
            #fig.show()
            fig.write_image('static/{}.jpg'.format(filename))
        """
        

    return {
        'code':'success'
    }
