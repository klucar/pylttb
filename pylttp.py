from lttb import lttb
from lttb import lttb2
from lttb import lttb3

import pandas as pd
import csv
from bokeh.charts import TimeSeries, show, output_file, hplot, gridplot
import datetime

downsample = lttb.largest_triangle_three_buckets
downsample2 = lttb2.largest_triangle_three_buckets
downsample3 = lttb3.largest_triangle_three_buckets


def get_plot_data(data):
    timestamps = [datetime.datetime.fromtimestamp(int(x[0]/1000)) for x in data]
    values = [x[1] for x in data]

    return dict(time=timestamps, values=values)


data = []
with open('data/exampledata1.txt', 'rb') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', fieldnames=['timestamp', 'value'])
    for row in reader:
        data.append((int(row['timestamp']),float(row['value'])))

factor = 20

down_data = downsample(data, len(data)/factor)
down_data2 = downsample2(data, len(data)/factor)
down_data3 = downsample3(data, len(data)/factor)

plt_raw = get_plot_data(data)
plt_down = get_plot_data(down_data)
plt_down2 = get_plot_data(down_data2)
plt_down3 = get_plot_data(down_data3)

plt_data = dict(raw=plt_raw['values'], rawtime=plt_raw['time'])
plt_data1 = dict(down=plt_down['values'], downtime=plt_down['time'])
plt_data2 = dict(down=plt_down2['values'], downtime=plt_down2['time'])
plt_data3 = dict(down=plt_down3['values'], downtime=plt_down3['time'])

tsline = TimeSeries(plt_data,
    x='rawtime', y='raw',
    title="Raw Timeseries:{}".format(len(plt_data['raw'])), ylabel='', legend=False)

tsline2 = TimeSeries(plt_data1,
    x='downtime', y='down',
    title="LTTB Timeseries:{}".format(len(plt_data1['down'])), ylabel='', legend=False)

tsline3 = TimeSeries(plt_data2,
    x='downtime', y='down',
    title="LTTB Max Timeseries:{}".format(len(plt_data2['down'])), ylabel='', legend=False)

tsline4 = TimeSeries(plt_data3,
    x='downtime', y='down',
    title="LTTB Min Timeseries:{}".format(len(plt_data3['down'])), ylabel='', legend=False)



AAPL = pd.read_csv(
    "http://ichart.yahoo.com/table.csv?s=AAPL&a=0&b=1&c=2000&d=0&e=1&f=2010",
    parse_dates=['Date'])
#MSFT = pd.read_csv(
#    "http://ichart.yahoo.com/table.csv?s=MSFT&a=0&b=1&c=2000&d=0&e=1&f=2010",
#    parse_dates=['Date'])
#IBM = pd.read_csv(
#    "http://ichart.yahoo.com/table.csv?s=IBM&a=0&b=1&c=2000&d=0&e=1&f=2010",
#    parse_dates=['Date'])
data = dict(
    AAPL=AAPL['Adj Close'],
    Date=AAPL['Date'],
#    MSFT=MSFT['Adj Close'],
#    IBM=IBM['Adj Close'],
)

dates = [val for val in data['Date'].values]
aapl = [val for val in data['AAPL'].values]
reworked_data = [(dates[x].astype(datetime.datetime)/1000000, aapl[x]) for x in range(0, len(dates),1)]

down_data = downsample(reworked_data, len(dates)/factor)
down_data2 = downsample2(reworked_data, len(dates)/factor)
down_data3 = downsample3(reworked_data, len(dates)/factor)

tsline5 = TimeSeries(data,
    x='Date', y=['AAPL'],
    color=['AAPL'], dash=['AAPL'],
    title="Timeseries:{}".format(len(data['Date'])), ylabel='Stock Prices', legend=True)

tsline6 = TimeSeries(get_plot_data(down_data),
    x='time', y='values',
    title="LTTB Timeseries:{}".format(len(down_data), ylabel='', legend=False))

tsline7 = TimeSeries(get_plot_data(down_data2),
    x='time', y='values',
    title="LTTB Max Timeseries:{}".format(len(down_data), ylabel='', legend=False))

tsline8 = TimeSeries(get_plot_data(down_data3),
    x='time', y='values',
    title="LTTB Min Timeseries:{}".format(len(down_data), ylabel='', legend=False))


output_file("timeseries.html")

show(gridplot([[tsline,tsline2,tsline3,tsline4],[tsline5,tsline6,tsline7,tsline8]]))

