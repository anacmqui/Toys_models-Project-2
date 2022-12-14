#First Part
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.ticker as mtick
import sqlalchemy as sql
import datetime

# conn = 'mysql://USER:PW@DBHOST/DB'
connection = 'mysql://toyscie:WILD4Rdata!@51.68.18.102:23456/toys_and_models'
sql_engine = sql.create_engine(connection)
query_sales = '''with productline_sales as (
    select productLine,
        monthname(orderDate) order_month,
                year(orderDate) order_year,
                DATE_FORMAT(orderDate, "%M %Y") as month_year,
                round(sum(quantityOrdered),0) total_orders
        from orders
        inner join orderdetails using (orderNumber)
        inner join products using (productCode)
        group by productLine, order_year, order_month
        )
select productline,  total_orders, order_month, order_year, month_year, LAG(total_orders, 1) over (
    partition by productLine, order_month
        order by productLine, month_year
        ) prev_year_order_total , (((total_orders - (LAG(total_orders, 1) over (
    partition by productLine, order_month
        order by  productLine, month_year
        )))/(LAG(total_orders, 1) over (
    partition by productLine
        order by  productLine, month_year ASC
        ))) *100) as growth
from productline_sales
order by  productLine, month_year'''
#!pip install mysql-connector
...
import mysql.connector
...
connection3 = mysql.connector.connect(user = 'toyscie', password = 'WILD4Rdata!', host = '51.68.18.102', port = '23456', database = 'toys_and_models')
...
dfSales = pd.read_sql(query_sales, con=connection3)
#dfSales = pd.read_sql_query(query_sales, sql_engine)
dfSales
# fig01, ax = plt.subplots(figsize = (15, 5))
# ax.bar(dfSales['productline'], dfSales['growth'])
# ax.set_ylabel('Overall Growth in Orders')
# ax.set_title('Product Lines')
# st.pyplot(fig01)

#Second Part
##Growth by category considering all dates##

fig01, ax = plt.subplots(figsize = (15, 5))
dfS = dfSales.groupby('productline').mean()
ax.bar(dfS.index, dfS['growth'])
#ax.bar(dfSales.groupby('productline').mean()[['growth']],height='growth')
#ax.bar(dfSales['productline'], dfSales['growth'])  #grwt
ax.set_ylabel('Overall Growth in Orders')
ax.set_xlabel('Product Lines')
ax.set_title('Growth by category (all_dates)')
#Put % in y axis
fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
xticks = mtick.FormatStrFormatter(fmt)
ax.yaxis.set_major_formatter(xticks)
st.pyplot(fig01)

#Third Part
#dfSales.groupby('productline').total_orders.sum()
print('Total orders in 2020')
print(dfSales[dfSales['order_year']==2020].groupby('productline').total_orders.sum())
print('')
st.text('Total orders in 2020')
st.table(dfSales[dfSales['order_year']==2020].groupby('productline').total_orders.sum())
print('Total orders in 2021')
print(dfSales[dfSales['order_year']==2021].groupby('productline').total_orders.sum())
print('')
st.text(" ")
st.text("Total orders 2021")
st.table(dfSales[dfSales['order_year']==2021].groupby('productline').total_orders.sum())

print('Total orders all years')
print(dfSales.groupby('productline').total_orders.sum())
st.text(" ")
st.text("Total orders all years")
st.table(dfSales.groupby('productline').total_orders.sum())


#Fourth Part
data2020 = dfSales[dfSales['order_year']==2020].groupby('productline').total_orders.sum()
data2021 = dfSales[dfSales['order_year']==2021].groupby('productline').total_orders.sum()
data2022 = dfSales[dfSales['order_year']==2022].groupby('productline').total_orders.sum()
dataAll = dfSales.groupby('productline').total_orders.sum()
labels = ['Classic Cars', 'Motorcycles', 'Planes', 'Ships', 'Trains',
       'Trucks and Buses', 'Vintage Cars']

#define Seaborn color palette
colors = sns.color_palette('tab10')[0:7]
colors1 = sns.color_palette('Paired')[0:7]

#Create pie chart for each year
#Year 2020
print('Plot 2020')
fig02,  ax = plt.subplots(figsize =(10, 5))
plt.pie(data2020, labels = labels, colors = colors1, autopct='%.0f%%')
#plt.show()
st.text(" ")
st.text("Plot 2020")
st.pyplot(fig02)
print('')

#Year 2021
print('Plot 2021')
fig03, ax = plt.subplots(figsize = (10,5))
plt.pie(data2021, labels = labels, colors = colors1, autopct='%.0f%%')
#plt.show()
st.text(" ")
st.text("Plot 2021")
st.pyplot(fig03)
print('')

#Year 2022
fig04, ax = plt.subplots(figsize =(5,5))
plt.pie(data2022, labels= labels, colors= colors1, autopct='%.0f%%' )
st.text(" ")
st.text("Plot 2022")
st.pyplot(fig04)

#All years
fig05, ax = plt.subplots(figsize = (5,5))
plt.pie(dataAll, labels = labels, colors = colors, autopct='%.0f%%')
st.text(" ")
st.text("Plot All")
st.pyplot(fig05)


#Fifth Part
# #Just with seaborn
# CC = dfSales[dfSales["productline"] == "Classic Cars"]
# orders_CC = dfSales[dfSales["productline"] == "Classic Cars"].total_orders.sum()
# fig06, ax = plt.subplots()
# sns.barplot(data=dfSales, x=CC, y=orders_CC, hue="order_month", ci=None)
# # sns.set(rc={'figure.figsize':(12,5)})
# st.pyplot(fig06)

#Final Part
#Only for classic cars , total orders each year
dfSales[dfSales['productline']=='Classic Cars']
dfCC = dfSales[dfSales['productline']=='Classic Cars']

fig07, ax = plt.subplots(figsize = (15, 5))
sns.barplot(data=dfCC, x='order_month', y="total_orders", hue="order_year", ci=None)
ax.set_ylabel('Orders')
ax.set_xlabel('Month')
ax.set_title('Monthly order growth for Classic Cars')
plt.legend(loc='upper right', title='Year')
st.pyplot(fig07)

fig08, ax = plt.subplots(figsize =(15,5))
sns.set(rc={'figure.figsize':(12,5)})
sns.barplot(data=dfCC, x='order_month', y="total_orders", hue="order_year", ci=None)
plt.legend(loc='upper right', title='Year')
st.pyplot(fig08)