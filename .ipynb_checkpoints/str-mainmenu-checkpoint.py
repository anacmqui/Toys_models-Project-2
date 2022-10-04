import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
#import sqlalchemy as sql
import datetime
import mysql.connector





#Query 1 - Define turnover of countries of last 2 months
query_fin = '''select customers.country, month(orders.orderDate) as 'Month', sum(orderdetails.quantityOrdered*orderdetails.priceEach) as Turnover
from orders
join orderdetails
on orderdetails.orderNumber = orders.orderNumber
join customers
on orders.customerNumber = customers.customerNumber
where status <>'Cancelled' and orders.orderDate>=date_sub(curdate(), interval 2 month)
group by country, monthname(orders.orderDate) desc;'''

#dffin

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


#Contact information of the clients overdue
query_fin3='''select customers.customerNumber as Customer_Number, customerName as Customer_Name, country as Country, concat(contactFirstName, ' ', contactLastName) as Contact_person, phone, count(orderNumber) as Total_orders from customers
join orders
on orders.customerNumber=customers.customerNumber
where customers.customerNumber = 141 or customers.customerNumber = 124 or customers.customerNumber = 448 or customers.customerNumber = 131 
or customers.customerNumber = 321 or customers.customerNumber = 186 or customers.customerNumber = 144 
or customers.customerNumber = 496 or customers.customerNumber = 333 or customers.customerNumber = 201 or customers.customerNumber = 219 or customers.customerNumber = 357
group by customers.customerNumber
;'''

#Table with contact info

query_sales = '''with productline_sales as (
select productLine,
month(orderDate) order_month,
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
    

query_logistics = '''select sum(products.quantityInStock), products.productName
from products
join orderdetails
on products.productCode = orderdetails.productCode
join orders
on orderdetails.orderNumber = orders.orderNumber
where not orders.status ='Cancelled'
group by products.productName
order by sum(orderdetails.quantityOrdered) desc limit 0,5'''

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
select concat(firstName, ' ', lastName) as Name, employeeNumber, final_amount, date_true, price_rank
from top_sellers
where date_true = ("06 2022") or date_true = ("07 2022") or date_true = ("08 2022")
having price_rank=1 or price_rank=2;'''

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

connection2 = mysql.connector.connect(user = 'toyscie', password = 'WILD4Rdata!', host = '51.68.18.102', port = '23456', database = 'toys_and_models')    
#connection3 = mysql.connector.connect(user = 'toyscie', password = 'WILD4Rdata!', host = '51.68.18.102', port = '23456', database = 'toys_and_models')
#connection = 'mysql://toyscie:WILD4Rdata!@51.68.18.102:23456/toys_and_models'
#sql_engine = sql.create_engine(connection) 

 
dffin = pd.read_sql_query(query_fin, con=connection2)    
dffin2 = pd.read_sql_query(query_fin2, con=connection2)
dffin2['customerNumber'] = dffin2['customerNumber'].astype(str)        
dffin3 = pd.read_sql_query(query_fin3, con=connection2)
dffin3.set_index('Customer_Number', drop = True)    
dfSales = pd.read_sql(query_sales, con=connection2)
dfLog = pd.read_sql_query(query_logistics, con=connection2)    
dffin_1 = pd.read_sql_query(query1_hr, con=connection2)
dffin_2 = pd.read_sql_query(query2_hr, con=connection2)



primaryColor = '#77FFE3'
    
st.title('Project 2!')


# Using object notation
add_selectbox = st.sidebar.selectbox(
    "Select company's department",
    ["Sales", "Finance","Logistics", "HR"],
    )    
    

# Query 1 plot
if add_selectbox == 'Finance':
    
    fig1, ax = plt.subplots(figsize = (10, 5))
    sns.barplot(data=dffin, x='country', y="Turnover", hue="Month", ci=None)
    ax.set_ylabel('Turnover')
    ax.set_xlabel('Country')
    ax.set_title('Where are orders going recently?')
    plt.legend(loc='upper left', title='Month')
    st.pyplot(fig1)
    
    fig2, ax = plt.subplots(figsize = (5, 5)) 
    sns.barplot(data=dffin2, x='customerNumber', y="to_be_paid", color='b')
    ax.set_ylabel('Amount to be paid')
    ax.set_xlabel('Customer Number')
    ax.set_title('Which clients do we have to chase?')
    plt.legend(loc='upper left')
    st.pyplot(fig2)
    
    st.table(dffin3) 

elif add_selectbox == 'Sales':
    st.markdown('''Welcome to *Sales*''')
    
    #connection = 'mysql://toyscie:WILD4Rdata!@51.68.18.102:23456/toys_and_models'
    #sql_engine = sql.create_engine(connection)
   

    fig01, ax = plt.subplots(figsize = (15, 5))
    dfS = dfSales.groupby('productline').mean()
    ax.bar(dfS.index, dfS['growth'])
    ax.set_ylabel('Overall Growth in Orders')
    ax.set_xlabel('Product Lines')
    ax.set_title('Growth by category (all_dates)')
    fmt = '%.0f%%' 
    xticks = mtick.FormatStrFormatter(fmt)
    ax.yaxis.set_major_formatter(xticks)
    st.pyplot(fig01)

    print('Total orders in 2020')
    print(dfSales[dfSales['order_year']==2020].groupby('productline').total_orders.sum())
    print('')
    #st.text('Total orders in 2020')
    #st.table(dfSales[dfSales['order_year']==2020].groupby('productline').total_orders.sum())
    
    print('Total orders in 2021')
    print(dfSales[dfSales['order_year']==2021].groupby('productline').total_orders.sum())
    print('')
    #st.text(" ")
    #st.text("Total orders 2021")
    #st.table(dfSales[dfSales['order_year']==2021].groupby('productline').total_orders.sum())

    print('Total orders all years')
    print(dfSales.groupby('productline').total_orders.sum())
    #st.text(" ")
    #st.text("Total orders all years")
    #st.table(dfSales.groupby('productline').total_orders.sum())

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
    #st.text(" ")
    #st.text("Plot 2020")
    #st.pyplot(fig02)
    
    #Year 2021
    print('Plot 2021')
    fig03, ax = plt.subplots(figsize = (10,5))
    plt.pie(data2021, labels = labels, colors = colors1, autopct='%.0f%%')
    #plt.show()
    #st.text(" ")
    #st.text("Plot 2021")
    #st.pyplot(fig03)

    #Year 2022
    fig04, ax = plt.subplots(figsize =(5,5))
    plt.pie(data2022, labels= labels, colors= colors1, autopct='%.0f%%' )
    #st.text(" ")
    #st.text("Plot 2022")
    #st.pyplot(fig04)

    #All years
    fig05, ax = plt.subplots(figsize = (5,5))
    plt.pie(dataAll, labels = labels, colors = colors, autopct='%.0f%%')
    st.text(" ")
    st.text("Plot All")
    st.pyplot(fig05)
    
    #dfSales[dfSales['productline']=='Classic Cars']
    
    options = st.selectbox('Choose the type of product:', ['Classic Cars', 'Vintage Cars', 'Planes', 'Motorcycles','Ships','Trains','Trucks and Buses'])
    
    
    #dfCC = dfSales[dfSales['productline']==options]

    fig07, ax = plt.subplots(figsize = (15, 5))
    sns.barplot(data=dfSales[dfSales['productline']==options], x='order_month', y="total_orders", hue="order_year", ci=None)
    ax.set_ylabel('Orders')
    ax.set_xlabel('Month')
    ax.set_title('Monthly order growth for Classic Cars')
    plt.legend(loc='upper right', title='Year')
    st.pyplot(fig07)

  
    
    #fig08, ax = plt.subplots(figsize =(15,5))
    #sns.set(rc={'figure.figsize':(12,5)})
    #sns.barplot(data=dfCC, x='order_month', y="total_orders", hue="order_year", ci=None)
    #plt.legend(loc='upper right', title='Year')
    #st.pyplot(fig08)

elif add_selectbox == 'Logistics':
    st.markdown('''Hi, _this_ is **Logistics**''')
    
    
    print(dfLog)


    st.title('Logistics')
    st.table(dfLog)
    
else:
    st.markdown('''Hi, _this_ is **HR**''')
    
    
# Query 1 plot
    fig_1, ax = plt.subplots(figsize = (5, 5))
    sns.barplot(data=dffin_1, x='date_true', y='final_amount', hue="Name", ci=None)
    ax.set_ylabel('Amount')
    ax.set_xlabel('Date')
    ax.set_title('The best sellers over the last 3 months')
    plt.legend(loc='upper left', title='Sellers')
    st.pyplot(fig_1)
    
# Query 2 plot

    st.dataframe(dffin_2)
