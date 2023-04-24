import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from env import username, password, host 
# --------------- FOR opsd_germany_daily DATA ------------------

def acquire_opsd_germany_daily():

    if os.path.isfile('opsd_germany_daily.csv'):
        return pd.read_csv('opsd_germany_daily.csv')
    
    else:

        url = 'https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv'
        df = pd.read_csv(url)
        df.to_csv('opsd_germany_daily.csv')

    return df

def prepare_opsd_germany_daily():

    df = acquire_opsd_germany_daily()

    df['Date'] = pd.to_datetime(df['Date'])

    df = df.set_index('Date').sort_index()

    df['month'] = df.index.month

    df['year'] = df.index.year

    df = df.fillna(0)

    df = df.drop(columns='Unnamed: 0')

    return df

def univariate_viz(df):

    for col in df.columns:
        print(f'Univariate Visualization of {col}')
        plt.hist(df[col], color='violet', edgecolor='black')
        plt.axvline(df[col].mean())
        plt.show()

def aqcuire_store_data():

    if os.path.isfile('tsa_store_data.csv'):
        return pd.read_csv('tsa_store_data.csv')
    
    else:
        print(f'Please download the CSV file and save it locally. Once saved as \'tsa_store_data.csv\', please rerun this function')

def get_db_url(database):
    return f'mysql+pymysql://{username}:{password}@{host}/{database}'

def get_store_data():
   
    query = '''
    SELECT *
    FROM items
    JOIN sales USING(item_id)
    JOIN stores USING(store_id) 
    '''
    
    df = pd.read_sql(query, get_db_url('tsa_item_demand'))
    
    df.to_csv('tsa_item_demand.csv', index=False)
    
    return df

def wrangle_store_data():
    filename = 'tsa_item_demand.csv'
    
    if os.path.isfile(filename):
        df = pd.read_csv(filename, index_col=0)
    else:
        df = get_store_data()
        
    return df

def prepare_store_data():

    df = wrangle_store_data()

    df['sale_date'] = pd.to_datetime(df.sale_date)

    df = df.set_index('sale_date').sort_index()

    df['month'] = df.index.month_name()

    df['day_of_week'] = df.index.day_name()

    df['sales_total'] = df.sale_amount * df.item_price

    return df

def sales_viz(df):

    plt.hist(df['sale_amount'], color='teal', edgecolor='black')
    plt.axvline(df.sale_amount.mean(), color='red', linestyle='dashed')
    plt.title('Distribution of Sales Amount')
    plt.xlabel('Sales (USD)')
    plt.ylabel('Count of Sales')
    plt.show()

    plt.hist(df['item_price'], color='turquoise', edgecolor='black')
    plt.axvline(df.item_price.mean(), color='red', linestyle='dashed')
    plt.title('Distribution of Item Prices')
    plt.xlabel('Prices (USD)')
    plt.ylabel('Count of Items')
    plt.show()

