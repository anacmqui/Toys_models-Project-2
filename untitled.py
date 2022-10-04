

query3_hr = ''' 
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
select concat(firstName, ' ', lastName) as Name, count(price_rank) from top_sellers
where price_rank=1 
group by lastname
order by count(price_rank) desc;'''

# 2ND  QUERY

df2 = pd.read_sql(query2_hr, con=connection2)
df2.head()

# TRY WITH THE STACKED = TRUE ELEMENT
df2.pivot(index='date_true', columns='Name', values ='final_amount').plot(kind='bar')
plt.suptitle("Who are your best sellers since the last 3 months?", size = 14)
plt.xlabel('Date')
plt.ylabel('Amount')
plt.show()

# 3RD  QUERY

df3 = pd.read_sql (query3_hr, con=connection2)
df3.head()



AUTRE;
col1, col2, col3 = st.columns(3)

with col1:
   st.header("The top 3 of yours sellers")
   st.image("https://static.streamlit.io/examples/person.jpg")