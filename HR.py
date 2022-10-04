import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
import streamlit as st
import seaborn as sns

from datetime import datetime

connection2 = mysql.connector.connect(user = 'toyscie', password = 'WILD4Rdata!', host = '51.68.18.102', port = '23456', database = 'toys_and_models')

#Query 1 - Show the best sellers since the last 3 months

query1_hr = '''
with top_sellers as (select employeeNumber, lastName, firstName, jobTitle, sum(priceEach*quantityOrdered) as final_amount,
 DATE_FORMAT(orders.orderdate, "%m %Y") as date_true, rank() over (partition by date_true order by final_amount desc) price_rank from employees
join customers
on employees.employeeNumber=customers.salesRepEmployeeNumber
join orders
on orders.customerNumber=customers.customerNumber
join orderdetails
on orders.orderNumber=orderdetails.orderNumber
where jobTitle like 'Sales Rep%' and orders.status <> 'Cancelled'
group by date_true, employees.employeeNumber
order by date_true, final_amount desc)
select concat(firstName, ' ', lastName) as Sellers, employeeNumber, final_amount, date_true, price_rank
from top_sellers
having price_rank=1 or price_rank=2;'''
dffin_1 = pd.read_sql_query(query1_hr, con=connection2)

# Query 1 plot
fig_1, ax = plt.subplots(figsize = (5, 5))
sns.barplot(data=dffin_1, x='date_true', y='final_amount', hue="Name", ci=None)
ax.set_ylabel('Amount')
ax.set_xlabel('Date')
ax.set_title('The best sellers over the last 3 months')
plt.legend(loc='upper left', title='Sellers')
st.pyplot(fig_1)

# Query 2 HR 

query2_hr = ''' 
with top_sellers as (select employeeNumber, lastName, firstName, jobTitle, sum(priceEach*quantityOrdered) as final_amount,
 DATE_FORMAT(orders.orderdate, "%m %Y") as date_true, rank() over (partition by date_true order by final_amount desc) price_rank from employees
join customers
on employees.employeeNumber=customers.salesRepEmployeeNumber
join orders
on orders.customerNumber=customers.customerNumber
join orderdetails
on orders.orderNumber=orderdetails.orderNumber
where jobTitle like 'Sales Rep%' and orders.status <> 'Cancelled'
group by date_true, employees.employeeNumber
order by date_true, final_amount desc)
select concat(firstName, ' ', lastName) as Name, count(price_rank) as Ranking from top_sellers
where Ranking=1 
group by lastname
order by Ranking desc;'''
dffin_2 = pd.read_sql_query(query2_hr, con=connection2)
st.dataframe(dffin_2)
    
 