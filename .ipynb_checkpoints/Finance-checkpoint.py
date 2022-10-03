import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
import streamlit as st

import sqlalchemy as sql
from datetime import datetime

connection2 = mysql.connector.connect(user = 'toyscie', password = 'WILD4Rdata!', host = '51.68.18.102', port = '23456', database = 'toys_and_models')
query_fin = '''select customers.country, month(orders.orderDate) as 'Month', sum(orderdetails.quantityOrdered*orderdetails.priceEach) as Turnover
from orders
join orderdetails
on orderdetails.orderNumber = orders.orderNumber
join customers
on orders.customerNumber = customers.customerNumber
where status <>'Cancelled' and orders.orderDate>=date_sub(curdate(), interval 2 month)
group by country, monthname(orders.orderDate) desc;'''
dffin = pd.read_sql_query(query_fin, con=connection2)
dffin

#st.table(dffin)

#dffin.pivot(index='country', columns ='Month', values ='Turnover').plot(kind='bar', title ='Where are orders going to recently?')
#plt.xlabel('Country')
#plt.ylabel('Ordered amount')
#st.pyplot(fig_viz)

fig, x = plt.subplots()

x.bar(dffin.pivot(index='country', columns ='Month', values ='Turnover').plot(kind='bar', title ='Where are orders going to recently?'),
plt.xlabel('Country'),
plt.ylabel('Ordered amount')
)

st.pyplot(fig)

query_fin2 = '''with amount_ordered as (select orders.customerNumber, sum(orderdetails.priceEach*orderdetails.quantityOrdered) as final_ordered from orderdetails
join orders
on orders.orderNumber = orderdetails.orderNumber
group by orders.customerNumber -- did not include status <> 'Cancelled' because the difference is negative for some, might mean that order was partially cancelled and part of it was paid
order by orders.customerNumber),
amount_paid as (select payments.customerNumber, sum(payments.amount) as final_paid from payments
group by payments.customerNumber
order by customerNumber)
select amount_ordered.customerNumber, final_ordered, final_paid, final_ordered-final_paid as to_be_paid from amount_paid
join amount_ordered
on amount_ordered.customerNumber = amount_paid.customerNumber
having to_be_paid <> 0
order by to_be_paid desc
;'''
dffin2 = pd.read_sql_query(query_fin2, con=connection2)
dffin2

dffin2['customerNumber'] = dffin2['customerNumber'].astype(str)

st.table(dffin2)

plt.title('Which clients do we have to chase?')
plt.bar(dffin2["customerNumber"],dffin2["to_be_paid"])
plt.xlabel('Customer Number')
plt.ylabel('Amount owed')
#st.plt()

query_fin3='''select customers.customerNumber as Customer_Number, customerName as Customer_Name, country as Country, concat(contactFirstName, ' ', contactLastName) as Contact_person, phone, count(orderNumber) as Total_orders from customers
join orders
on orders.customerNumber=customers.customerNumber
where customers.customerNumber = 141 or customers.customerNumber = 124 or customers.customerNumber = 448 or customers.customerNumber = 131 
or customers.customerNumber = 321 or customers.customerNumber = 186 or customers.customerNumber = 144 
or customers.customerNumber = 496 or customers.customerNumber = 333 or customers.customerNumber = 201 or customers.customerNumber = 219 or customers.customerNumber = 357
group by customers.customerNumber
;'''

dffin3 = pd.read_sql_query(query_fin3, con=connection2)
dffin3

st.table(dffin3)
