import os
import pandas as pd
import random
import string
import numpy as np

# Set the data directory path
data_dir = '/Users/stak/dev/Customer_Success_Dashboard/data'

# Create a function to generate random purchase dates
def generate_purchase_date():
    return pd.to_datetime('2020-01-01') + pd.DateOffset(days=random.randint(0, 1200))

# Create a function to generate snapshot dates based on the purchase date
def generate_snapshot_dates(purchase_date, n_months):
    snapshot_dates = pd.date_range(start=purchase_date, periods=n_months, freq='M')
    return snapshot_dates

# Create a function to generate random customer names
def generate_name():
    first_names = ['Raphael', 'Richard', 'Thomas', 'Ahmed', 'Andre', 'Caden', 'Dallas', 'Eric', 'Ermias', 'Evan', 'Hayden', 'Ismael', 'Jamir', 'Jaylen', 'Kaden', 'Leon', 'Ava', 'Madison', 'Skylar', 'Riley', 'Amelia', 'Olivia', 'Zuri', 'Isabella', 'Fatoumata', 'Serenity', 'Zoey', 'Chloe', 'Aria', 'Fatima', 'Leah', 'Melody', 'Amina', 'Mariam', 'Nova', 'Aaliyah', 'Brielle', 'Layla', 'Mia', 'Grace', 'Nyla', 'Sophia', 'Aisha', 'Kylie', 'Miracle', 'Wynter', 'Autumn', 'Kayla', 'Kehlani', 'Reign', 'Savannah']
    last_names = ['SMITH', 'JOHNSON', 'WILLIAMS', 'BROWN', 'JONES', 'MILLER', 'DAVIS', 'GARCIA', 'RODRIGUEZ', 'WILSON', 'MARTINEZ', 'ANDERSON', 'TAYLOR', 'THOMAS', 'HERNANDEZ', 'MOORE', 'MARTIN', 'JACKSON', 'THOMPSON', 'WHITE', 'LOPEZ', 'LEE']
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return first_name, last_name

# Function to update contract status and MRR for a specific month within the contract year
def update_contract_status_and_mrr_for_month(row):
 # Extract the current contract status, MRR, and CustomerID
    contract_status = row.get('ContractStatus', 'Active')
    current_mrr = row.get('MRR', 0)
    customer_id = row.get('CustomerID')
    contract_year = row.get('ContractYears')

    termination_prob, upsell_prob, downsell_prob = random.uniform(0.01, 0.2), random.uniform(0.10, 0.40), random.uniform(0.10, 0.20)

    if random.random() < termination_prob:
        new_contract_status, new_mrr = 'Churned', 0
    elif random.random() < upsell_prob:
        new_contract_status, new_mrr = 'Upsell', current_mrr * random.uniform(1, 5)
    elif random.random() < downsell_prob:
        new_contract_status, new_mrr = 'Downsell', current_mrr * random.uniform(0.2, 0.9)
    else:
        new_contract_status, new_mrr = 'Active', current_mrr

    return pd.Series({'CustomerID': customer_id, 'ContractStatus': new_contract_status, 'MRR': round(new_mrr, -1), 'ContractYears': contract_year})

# Create a function to generate random verticals
def generate_vertical():
    verticals = ['Consultants', 'Non-Profit', 'Entertainment', 'Restaurants', 'Travel']
    return random.choice(verticals)

# Create a function to generate random MRR
def generate_mrr():
    return max(round(np.random.normal(1500, 550), -1), 100)

# Create a function to generate random support tickets
def generate_support_tickets():
    return random.randint(0, 10)

# Create a function to generate random CSAT scores
def generate_csat():
    return round(random.uniform(0, 5), 2)

# Set the number of customers and months
n_customers = 1000
n_months = 36
#snp_dte = '2020-01-01'

#snapshot_dates = generate_snapshot_dates(snp_dte,n_months)

## Export snapshot dates to a CSV file
#snapshot_dates.to_frame(name='SnapshotDate').to_csv('snapshot_dates.csv', index=False)

# Create a data directory if it doesn't exist
os.makedirs(data_dir, exist_ok=True)

def generate_customer_data(n_customers, n_months):
    data = []

    for _ in range(n_customers):
        customer_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        first_name, last_name = generate_name()
        state = random.choice(['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL',
                              'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MT', 'NE', 'NV', 'NH',
                              'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO',
                              'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'])
        
        # Generate a random purchase date for each customer
        purchase_date = generate_purchase_date()
        vertical = generate_vertical()

        contract_months = 0
        contract_years = 0
        mrr = generate_mrr()
        support_tickets = generate_support_tickets()
        csat = generate_csat()

        # Calculate the end date for snapshots
        end_date = purchase_date + pd.DateOffset(months=n_months)
        snapshot_dates = pd.date_range(start=purchase_date, end=end_date, freq='M')

        for snapshot_date in snapshot_dates:
            # Calculate the contract months and years
            relationship_months = (snapshot_date - purchase_date).days // 30 + 1
            contract_months = relationship_months % 12 + 1
            contract_years = relationship_months  // 12 + 1

            # Reset contract months after every 12 months
            contract_months_in_year = (contract_months - 1) % 12 + 1

            data.append([customer_id, first_name, last_name, state, purchase_date, snapshot_date, relationship_months, contract_years, contract_months, vertical, mrr, support_tickets, csat])

    df = pd.DataFrame(data, columns=['CustomerID', 'FirstName', 'LastName', 'State', 'FirstPurchaseDate', 'SnapshotDate', 'RelationshipTerm', 'ContractYears', 'ContractMonths', 'Vertical', 'MRR', 'SupportTickets', 'AverageCSAT'])
    return df

# Example usage
n_customers = 2000  # You can change the number of customers as needed
n_months = 36  # Number of months for snapshots

# Generate customer data
customer_df = generate_customer_data(n_customers, n_months)
#customer_df = customer_df[customer_df['ContractMonths'] >= 1]

# Check if 'ContractStatus' column exists in the DataFrame; if not, add it with 'Active' as the default value
if 'ContractStatus' not in customer_df.columns:
    customer_df['ContractStatus'] = 'Active'

# Save customer data to CSV files
customer_df.to_csv(os.path.join(data_dir, 'customer_detail_data_rough.csv'), index=False)

# Assuming you have a DataFrame named 'customer_df'
contract_month_1_rows = customer_df[customer_df['ContractMonths'] == 1]

# Select the columns you want to display
result = contract_month_1_rows[['CustomerID', 'ContractYears', 'ContractMonths', 'MRR']]

# Create a new DataFrame for validation
validation_result = result.apply(update_contract_status_and_mrr_for_month, axis=1)

# Display the result
result.to_csv(os.path.join(data_dir, 'contract_month_1_rows.csv'), index=False)

# Display the result
validation_result.to_csv(os.path.join(data_dir, 'validation_result.csv'), index=False)

# Assuming 'customer_df' and 'validation_results' are DataFrames
customer_df_final = customer_df.merge(validation_result[['CustomerID', 'ContractYears', 'MRR', 'ContractStatus']],
                                on=['CustomerID', 'ContractYears'],
                                how='left')

customer_df_final['MRR'] = customer_df_final['MRR_y'].combine_first(customer_df_final['MRR_x'])
customer_df_final['ContractStatus'] = customer_df_final['ContractStatus_y'].combine_first(customer_df_final['ContractStatus_x'])

# Drop the columns MRR_x, MRR_y, ContractStatus_x, and ContractStatus_y
customer_df_final.drop(columns=['MRR_x', 'MRR_y', 'ContractStatus_x', 'ContractStatus_y'], inplace=True)

# # Save customer data to CSV files
customer_df_final.to_csv(os.path.join(data_dir, 'customer_detail_data_.csv'), index=False)

# Create MRR data
mrr_data = customer_df_final[['SnapshotDate', 'MRR']].groupby('SnapshotDate').sum().reset_index()
mrr_data.to_csv(os.path.join(data_dir, 'mrr_data.csv'), index=False)

# Create support tickets data
support_tickets_data = customer_df_final[['SnapshotDate', 'SupportTickets']].groupby('SnapshotDate').sum().reset_index()
support_tickets_data.to_csv(os.path.join(data_dir, 'support_tickets_data.csv'), index=False)

# Create total customer base summary
total_customer_base_summary = customer_df_final.groupby('SnapshotDate')['CustomerID'].count().reset_index()
total_customer_base_summary.to_csv(os.path.join(data_dir, 'total_customer_base_summary.csv'), index=False)

# # Create new customers summary
new_customers_summary = customer_df_final[customer_df_final['ContractStatus'] == 'Active'].groupby('SnapshotDate')['CustomerID'].count().reset_index()
new_customers_summary.to_csv(os.path.join(data_dir, 'new_customers_summary.csv'), index=False)

# # Create combined summary
combined_summary = pd.merge(total_customer_base_summary, mrr_data, on='SnapshotDate')
combined_summary = pd.merge(combined_summary, support_tickets_data, on='SnapshotDate')
combined_summary = pd.merge(combined_summary, new_customers_summary, on='SnapshotDate')
combined_summary.to_csv(os.path.join(data_dir, 'combined_summary.csv'), index=False)
