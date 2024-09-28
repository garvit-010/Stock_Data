import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

sns.set(style="whitegrid")

def intraday(stock, day, nxt_day):
    day = datetime.strptime(day, '%d/%m/%Y').strftime('%Y-%m-%d')
    nxt_day = datetime.strptime(nxt_day, '%d/%m/%Y').strftime('%Y-%m-%d')
    stock_data = yf.download(stock, start=day, end=nxt_day, interval="1m")
    stock_data['Time'] = stock_data.index.strftime('%H:%M')
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='Time', y='Close', data=stock_data, label='Closing Price', marker='o', color='b')
    
    plt.title(f'{stock} Intraday Price Behavior on {day}')
    plt.xlabel('Time (HH:MM)')
    plt.ylabel('Price (INR)')
    plt.xticks(rotation=45)  
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    return stock_data  # Return the data for export

def weekly_data(stock):
    stock_data = yf.download(stock, period="5d", interval="1d")
    stock_data.index = stock_data.index.strftime('%d/%m/%Y')

    plt.figure(figsize=(12, 6))
    sns.lineplot(x=stock_data.index, y='Close', data=stock_data, marker='o', label='Closing Price', color='b')
    
    plt.title(f'{stock} Weekly Closing Price')
    plt.xlabel('Date (DD/MM/YYYY)')
    plt.ylabel('Price (INR)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    return stock_data  # Return the data for export

def monthly_data(stock):
    stock_data = yf.download(stock, period="1y", interval="1mo")
    stock_data['Month'] = stock_data.index.strftime('%B %Y')

    plt.figure(figsize=(12, 6))
    sns.lineplot(x='Month', y='Close', data=stock_data, marker='o', label='Closing Price', color='b')

    plt.title(f'{stock} Monthly Closing Price Over the Past Year')
    plt.xlabel('Month')
    plt.ylabel('Price (INR)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    return stock_data  # Return the data for export

def all_time_data(stock):
    stock_data = yf.download(stock)

    plt.figure(figsize=(12, 6))
    sns.lineplot(x=stock_data.index, y='Close', data=stock_data, label='Closing Price', marker='o', color='b')

    plt.title(f'{stock} All-Time Closing Price')
    plt.xlabel('Date')
    plt.ylabel('Price (INR)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    return stock_data  # Return the data for export

def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def export_data(stock_data, stock, filename):
    stock_data.to_csv(filename, index=True)
    print(f"Data exported to {filename}")

print("Hi, Please select the service: ")
print("1. Intraday Data of a stock.")
print("2. Weekly Data of a stock.")
print("3. Monthly Data of a stock in a year.")
print("4. All time data of a stock.")

choice = [1, 2, 3, 4]

user_input = int(input("Enter your choice: "))
stock = input("Enter the stock symbol (ex., 'RELIANCE.NS'): ")

if user_input == 1:
    while True:
        day = input("Enter the date (DD/MM/YYYY) for the intraday data: ")
        nxt_day = input("Enter the next day (DD/MM/YYYY) to end the intraday data: ")
        if is_valid_date(day) and is_valid_date(nxt_day):
            data = intraday(stock, day, nxt_day)
            export_option = input("Do you want to download this data? (yes/no): ").strip().lower()
            if export_option == 'yes':
                filename = input("Enter the filename (ex., 'intraday_data.csv'): ")
                export_data(data, stock, filename)
            break
        else:
            print("Invalid date format. Please enter the date in DD/MM/YYYY format.")
elif user_input == 2:
    data = weekly_data(stock)
    export_option = input("Do you want to download this data? (yes/no): ").strip().lower()
    if export_option == 'yes':
        filename = input("Enter the filename (ex., 'weekly_data.csv'): ")
        export_data(data, stock, filename)
elif user_input == 3:
    data = monthly_data(stock)
    export_option = input("Do you want to download this data? (yes/no): ").strip().lower()
    if export_option == 'yes':
        filename = input("Enter the filename (ex., 'monthly_data.csv'): ")
        export_data(data, stock, filename)
elif user_input == 4:
    data = all_time_data(stock)
    export_option = input("Do you want to download this data? (yes/no): ").strip().lower()
    if export_option == 'yes':
        filename = input("Enter the filename (ex. 'all_time_data.csv'): ")
        export_data(data, stock, filename)
else:
    print("Invalid choice. Please select a valid option.")
