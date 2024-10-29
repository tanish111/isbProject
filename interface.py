import streamlit as st
import pandas as pd
import ast

# Load the data
DATA_PATH = 'merged_Manager_tickers_Data.csv'
manager_ticker_data = pd.read_csv(DATA_PATH)

# Function to update the CSV file
def update_csv(dataframe, file_path):
    dataframe.to_csv(file_path, index=False)

st.title('Fund Ticker Management')

# Create a placeholder to track if changes have been made
changes_made = False

# Pagination
funds_per_page = 20
total_funds = len(manager_ticker_data)
total_pages = (total_funds + funds_per_page - 1) // funds_per_page

# Page selector
page = st.selectbox('Select Page', range(1, total_pages + 1))

# Calculate the start and end indices of the funds to display
start_idx = (page - 1) * funds_per_page
end_idx = start_idx + funds_per_page

# Iterate through each row in the DataFrame for the current page
for index, row in manager_ticker_data.iloc[start_idx:end_idx].iterrows():
    st.subheader(f"Fund: {row['fund_name']}")
    parsed_data_tickers = ast.literal_eval(row['tickers'])
    if isinstance(parsed_data_tickers,list) and len(parsed_data_tickers) > 0 and isinstance(parsed_data_tickers[0],tuple):
        current_tickers = parsed_data_tickers
    else:
        current_tickers = [item for sublist in parsed_data_tickers for item in sublist]
    st.write("Current tickers:", current_tickers)
    parsed_data_prospectus_tickers = ast.literal_eval(row['prospectus_tickers'])
    if isinstance(parsed_data_prospectus_tickers, list) and len(parsed_data_prospectus_tickers) > 0 and isinstance(parsed_data_prospectus_tickers[0], tuple):
        prospectus_tickers = parsed_data_prospectus_tickers
    else:
        prospectus_tickers = [item for sublist in parsed_data_prospectus_tickers for item in sublist]

    # Add tickers
    add_tickers = st.multiselect(
        f"Add Tickers to {row['fund_name']}",
        [ticker for ticker in prospectus_tickers if ticker not in current_tickers],
        key=f"add_{index}"
    )
    if add_tickers:
        current_tickers.extend(add_tickers)
        st.success(f"Tickers '{', '.join(add_tickers)}' added.")
        changes_made = True

    # Remove tickers
    remove_tickers = st.multiselect(
        f"Remove Tickers from {row['fund_name']}",
        current_tickers,
        key=f"remove_{index}"
    )
    if remove_tickers:
        for ticker in remove_tickers:
            current_tickers.remove(ticker)
        st.warning(f"Tickers '{','.join([str(x) for x in remove_tickers])}' removed.")
        changes_made = True

    # Update the DataFrame with the new tickers
    manager_ticker_data.at[index, 'tickers'] = "["+','.join([str(x) for x in current_tickers])+"]"

# Save button
if st.button('Save Changes'):
    if changes_made:
        update_csv(manager_ticker_data, DATA_PATH)
        st.success('CSV file updated successfully!')
    else:
        st.info('No changes made.')
