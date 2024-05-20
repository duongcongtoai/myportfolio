import numpy_financial as npf
from datetime import datetime
from pyxirr import xirr
import pandas as pd

def read_cash_flows(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    # Ensure the date column is in datetime format
    df['date'] = pd.to_datetime(df['date'],format='%d/%m/%Y')
    # Convert the DataFrame columns to lists
    dates = df['date'].tolist()
    # cash_flows = df['amount'].tolist()
    # cash_flows = [float(i.replace(',', '')) for i in cash_flows]
    n_share = [int(i.replace(',', '')) for i in df['n_share'].tolist()]
    df['date'] = dates
    # df['amount'] = cash_flows
    df['n_share'] = n_share
    df = df.sort_values(by='date')
    return df

def calculate_xirr(dates, cash_flows):
    # Use numpy_financial's xirr function to calculate the internal rate of return
    irr = xirr(list(zip(dates, cash_flows)))
    return irr

def main():
    price = 17500
    file_path = 'total.csv'  # Update this with the actual file path
    df_by_date_asc = read_cash_flows(file_path)
    # append to df a new cashflow, as if the user wants to sell 
    # all of the amount accumualted with a given price

    sell_cashflow = df_by_date_asc['n_share'].sum()
    # set sell_date = current date instead
    sell_date = datetime.now() 
    # sell_date = pd.to_datetime('2021-06-01',format='%Y-%m-%d')
    df_by_date_asc = df_by_date_asc.append({'date': sell_date, 'amount': sell_cashflow*price}, ignore_index=True)
    dates = df_by_date_asc['date'].tolist()
    cash_flows = df_by_date_asc['amount'].tolist()
    irr = calculate_xirr(dates, cash_flows)
    print(f"XIRR: {irr * 100:.2f}%")

if __name__ == "__main__":
    # create a string with format 'YYYY-MM-DD' with value of now
    main()