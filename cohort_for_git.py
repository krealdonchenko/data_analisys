import pandas as pd
import numpy as np
# %load_ext google.colab.data_table
from vega_datasets import data

# Файл загружаем в gdrive - получаем ссылку с доступом для всех
# берем часть ссылки и ее маунтим

"""https://drive.google.com/file/d/1br8a4UBe8GIW3vIRFIPNpOk7J3PNm_OH/view?usp=sharing

https://drive.google.com/file/d/1-Fjs44hO-O1iM_GGGGiraViqvAc9WKdq/view?usp=sharing
"""

!gdown --id 1br8a4UBe8GIW3vIRFIPNpOk7J3PNm_OH
!gdown --id 1-Fjs44hO-O1iM_GGGGiraViqvAc9WKdq

df1 = pd.read_csv('/content/olist_orders_dataset.csv')
df2 = pd.read_csv('/content/olist_order_payments_dataset.csv')

# склеиваем два df
df = df1.merge(df2,on = 'order_id')

df.head()

# посмотрим все пропуски и форматы
df.info()

# меняем формат даты
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df['date'] = df['order_purchase_timestamp'].dt.strftime('%Y-%m')

# получаем дату первой покупки - она будет когортой
min_user_date = df.groupby('customer_id')['date'].min()

#склеиваем с df
df = df.merge(min_user_date,on='customer_id',suffixes=('_', 'min'))

# формируем когорту
cohorts = df.groupby(['datemin', 'date_'])\
['customer_id','payment_value','order_id'].agg(
    {'customer_id': pd.Series.nunique,
        'payment_value': 'sum',
          'order_id': 'count'})



