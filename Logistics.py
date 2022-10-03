import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sqlalchemy as sql
import datetime

connection = 'mysql://toyscie:WILD4Rdata!@51.68.18.102:23456/toys_and_models'
sql_engine = sql.create_engine(connection) 

query_logistics = '''select sum(products.quantityInStock), products.productName
from products
join orderdetails
on products.productCode = orderdetails.productCode
join orders
on orderdetails.orderNumber = orders.orderNumber
where not orders.status ='Cancelled'
group by products.productName
order by sum(orderdetails.quantityOrdered) desc limit 0,5'''

dfLog = pd.read_sql_query(query_logistics, sql_engine)
print(dfLog)


st.title('Logistics')
st.table(dfLog)
