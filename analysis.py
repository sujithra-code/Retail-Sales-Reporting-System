import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

df = pd.read_csv("train.csv")
df = df.dropna()           # remove missing values
df = df.drop_duplicates()  # remove duplicates
print(df.head())
print(df.info())
df.columns = df.columns.str.replace(" ", "_")      #if col  name with space - then store space as _  in df , Product_Name 
print(df.columns)



df["Order_Date"]=pd.to_datetime(df["Order_Date"],dayfirst=True)
# creates new column "month" , column with month values from "Order Date" - seasonal pattern (Which month performs best overall?)
df["Month"]=df["Order_Date"].dt.month                                                          
# creates new column "yearmonth" , This creates a Period datatype column. column with year values from "Order Date" - want timeline analysis (Month-by-month growth) , sales move month by month from 2016 to 2018
df["YearMonth"] = df["Order_Date"].dt.to_period("M").astype(str)


print("\n========== SQL SALES REPORT ==========")


# create Db connection - sales.db file created 
# Pandas df➜ SQL db
conn=sqlite3.connect("sales_reporting.db")   
df.to_sql("table_sales",conn,if_exists="replace",index=False)

# Total Sales:
query="""
SELECT SUM(Sales) as Total_Sales
FROM table_sales
"""
Total_Sales=pd.read_sql_query(query,conn)
print("\n Total Sales:")
print(Total_Sales)

# Sales by Region (SQL)
query="""
SELECT Region, SUM(Sales) as Total_Sales
FROM table_sales
GROUP BY Region
ORDER BY Total_Sales DESC;
"""
# run sql query- bring result back into pandas df
region_sales=pd.read_sql_query(query,conn)
print("\nSales by Region:")
print(region_sales)


# Sales by Category (SQL)
query="""
SELECT Category, SUM(Sales) as Total_Sales
FROM table_sales
GROUP BY Category
ORDER BY Total_Sales DESC;
"""
category_sales=pd.read_sql_query(query,conn)
print("\nSales by Category:")
print(category_sales)


# Sales by Product (SQL)
query="""
SELECT Product_Name, SUM(Sales) as Total_Sales
FROM table_sales
GROUP BY Product_Name
ORDER BY Total_Sales DESC
LIMIT 5;
"""
product_sales=pd.read_sql_query(query,conn)
print("\nSales by Product:")
print(product_sales)


# Sales by Month (SQL)
query="""
SELECT Month, SUM(Sales) as Total_Sales
FROM table_sales
GROUP BY Month
ORDER BY Total_Sales DESC;
"""
month_sales=pd.read_sql_query(query,conn)
print("\nSales by Month:")
print(month_sales)


# Sales by Year-Month (SQL)
query="""
SELECT YearMonth, SUM(Sales) as Total_Sales
FROM table_sales
GROUP BY YearMonth
ORDER BY Total_Sales DESC;
"""
year_month_sales=pd.read_sql_query(query,conn)
print("\nSales by YearMonth:")
print(year_month_sales)

conn.close()





                                        #    Matplotlib Visualization

# bar chart 
region_sales = df.groupby("Region")["Sales"].sum()
region_sales.plot(kind="pie")
plt.title("Sales by Region")

plt.ylabel("Total Sales")
plt.show()


category_sales.plot(kind="bar")
plt.title("Sales by Category")
plt.xlabel("category")
plt.ylabel("Total Sales")
plt.show()


# Line chart
monthly_sales=df.groupby("Month")["Sales"].sum()
monthly_sales.plot(kind="line")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.show()



year_month_sales=df.groupby("YearMonth")["Sales"].sum()
year_month_sales.plot(kind="line",figsize=(10,5))
plt.title("Monthly Sales Trend Over Time")
plt.xlabel("Year-Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.show()











# print("\nTotal Sales:")
# print(df["Sales"].sum())


# print("\nSales by region:")
# region_sales=df.groupby("Region")["Sales"].sum()
# print(region_sales)


# print("\nSales by Category:")
# category_sales=df.groupby("Category")["Sales"].sum()
# print(category_sales)



# print("\nProduct Name by Sales:")
# print(df.groupby("Product Name")["Sales"].sum())


# print("\nTop 5 sub-category by Sales:")
# sub_category_sales=df.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False)
# print(sub_category_sales.head())                                                         #check only 5 rows , not whole df 



# # df["Order Date"]=pd.to_datetime(df["Order Date"],dayfirst=True)



# # # creates new column "month" , column with month values from "Order Date" - seasonal pattern (Which month performs best overall?)
# # df["Month"]=df["Order Date"].dt.month                                                          
# # # creates new column "yearmonth" , This creates a Period datatype column. column with year values from "Order Date" - want timeline analysis (Month-by-month growth) , sales move month by month from 2016 to 2018
# # df["YearMonth"] = df["Order Date"].dt.to_period("M").astype(str)


# # print("\n Monthly sales:")
# # print(df.groupby("Month")["Sales"].sum().sort_values(ascending=False))
# # print("\n Year+Month:") 
# # print(df.groupby("YearMonth")["Sales"].sum().sort_values(ascending=False))



