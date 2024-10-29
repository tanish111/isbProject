import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('Manager_Ticker_Data.csv')

# Group by 'fund_name' and aggregate tickers and prospectus_tickers into a set (union)
merged_df = df.groupby('fund_name').agg({
    'tickers': lambda x: ','.join(set(x)),
    'prospectus_tickers': lambda x: ','.join(set(x))
}).reset_index()

# Save the result to a new CSV file
merged_df.to_csv('merged_Manager_tickers_Data.csv', index=False)

print('Merged tickers and prospectus_tickers have been saved to merged_Manager_tickers_Data.csv')