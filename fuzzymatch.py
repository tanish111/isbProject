import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re

def fuzzymatch(str1, str2):
    return fuzz.token_set_ratio(str1, str2)

# Load the blackrock_manager data into a DataFrame
blackrock_manager_df = pd.read_csv('Manager_Data.csv')
blackrock_manager_df['tickers'] = [[] for _ in range(len(blackrock_manager_df))]
blackrock_manager_df['prospectus_tickers'] = [[] for _ in range(len(blackrock_manager_df))]
flaged_funds = pd.read_csv('Manager_Data_Flaged.csv')
# Save the DataFrame to output.csv
ticker_df = pd.read_csv('output.csv')

# Get unique 'file_url' from both DataFrames
unique_blackrock_company_name = blackrock_manager_df['company_name'].unique()
for company in unique_blackrock_company_name:
    blackrock_dfs_each = blackrock_manager_df[blackrock_manager_df['company_name'] == company]
    ticker_dfs_each = ticker_df[ticker_df['company_name'] == company]
    for _, blackrock_row in blackrock_dfs_each.iterrows():
        if blackrock_row['fund_name'] in flaged_funds['fund_name'].values:
            continue
        ticker_dfs_each = ticker_dfs_each.drop_duplicates(subset='ticker')
        for _, ticker_row in ticker_dfs_each.iterrows():
            matchValue = fuzzymatch(blackrock_row['fund_name'], ticker_row['fund_name'])
            if matchValue > 95:
                blackrock_manager_df.loc[blackrock_row.name, 'tickers'].append((ticker_row['ticker'], ticker_row['fund_name']))
            elif matchValue > 70:
                blackrock_manager_df.loc[blackrock_row.name, 'prospectus_tickers'].append((ticker_row['ticker'], ticker_row['fund_name'],matchValue)) 
            else:
                pass

blackrock_manager_df.to_csv('Manager_Ticker_Data.csv', index=False)