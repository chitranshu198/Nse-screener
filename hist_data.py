from nsepy import get_history
from datetime import date
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
sbin = get_history(symbol='CHOLAFIN',
                   start=date(2021,10,30),
                   end=date(2022,1,30))



sbin.ta.sma(close='close', length=5, append=True)
sbin.ta.rsi(close='close', length=14, append=True)
df=sbin

fig = go.Figure(data=[
    go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        increasing_line_color='#ff9900',
        decreasing_line_color='black',
        showlegend=False,
    ),
])

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

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df['SMA_5'],
        line=dict(color='#ff9900', width=2),
        name='SMA_5'
    )
)

fig.show()

print(sbin)

