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

# Function to simulate customer churn or upsell
def simulate_churn_upsell(row):
    termination_prob = random.uniform(0.20, 0.50)
    upsell_prob = random.uniform(0.01, 0.40)
    downsell_prob = random.uniform(0.10, 0.30)

    # Calculate the contract month
    contract_months = (row['SnapshotDate'] - row['FirstPurchaseDate']).days // 30 % 12

    if contract_months > 12:
        if random.random() < termination_prob:
            return 'Churned'
        elif random.random() < upsell_prob:
            return 'Upsell'
        elif random.random() < downsell_prob:
            return 'Downsell'
    
    return 'Active'

# Function to generate contract status
def calculate_contract_status(snapshot_date, purchase_date):
    contract_months = ((snapshot_date - purchase_date).days // 30) + 1
    if contract_months < 0:
        return 'Active'
    elif contract_months < 12:
        return 'Active'
    elif contract_months == 12:
        return 'Active'
    else:
        termination_prob = random.uniform(0.01, 0.2)
        upsell_prob = random.uniform(0.10, 0.40)
        downsell_prob = random.uniform(0.10, 0.30)
        if random.random() < termination_prob:
            return 'Churned'
        elif random.random() < upsell_prob:
            return 'Upsell'
        elif random.random() < downsell_prob:
            return 'Downsell'
        else:
            return 'Active'

# Function to update contract status and MRR
def update_contract_status_and_mrr(row):
    # Extract the current contract status and MRR
    contract_status = row.get('ContractStatus', 'Active')
    current_mrr = row.get('MRR', 0)

    # Update contract status based on the existing status
    if contract_status == 'Churned':
        # For 'Churned', set MRR to 0
        new_contract_status = 'Churned'
        new_mrr = 0
    elif contract_status == 'Upsell':
        # For 'Upsell', increase MRR by a randomized value between 1 and 5
        mrr_increase = random.uniform(1, 5)
        new_contract_status = 'Active'
        new_mrr = current_mrr * mrr_increase
    elif contract_status == 'Downsell':
        # For 'Downsell', decrease MRR by a randomized value between 0.2 and 0.9
        mrr_decrease = random.uniform(0.2, 0.9)
        new_contract_status = 'Active'
        new_mrr = current_mrr * mrr_decrease
    else:
        # For 'Active' customers, maintain MRR and contract status
        new_contract_status = contract_status
        new_mrr = current_mrr

    return pd.Series({'ContractStatus': new_contract_status, 'MRR': new_mrr})

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
n_months = 24
snp_dte = '2020-01-01'

snapshot_dates = generate_snapshot_dates(snp_dte,n_months)

# Export snapshot dates to a CSV file
snapshot_dates.to_frame(name='SnapshotDate').to_csv('snapshot_dates.csv', index=False)

# Create a data directory if it doesn't exist
os.makedirs(data_dir, exist_ok=True)

# Create customer data
def generate_customer_data(n_customers, snapshot_dates):
    data = []

    for _ in range(n_customers):
        customer_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        first_name, last_name = generate_name()
        state = random.choice(['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL',
                              'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MT', 'NE', 'NV', 'NH',
                              'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO',
                              'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'])
        purchase_date = generate_purchase_date()
        vertical = generate_vertical()
        
        for snapshot_date in snapshot_dates:
            mrr = generate_mrr()
            support_tickets = generate_support_tickets()
            csat = generate_csat()
            contract_months = ((snapshot_date - purchase_date).days // 30) + 1
            data.append([customer_id, first_name, last_name, state, purchase_date,snapshot_date,contract_months, vertical, mrr, support_tickets, csat])

    df = pd.DataFrame(data, columns=['CustomerID', 'FirstName', 'LastName', 'State', 'FirstPurchaseDate','SnapshotDate', 'ContractMonths','Vertical',  'MRR', 'SupportTickets', 'AverageCSAT'])
    return df

# Generate customer data
customer_df = generate_customer_data(n_customers, snapshot_dates)
customer_df = customer_df[customer_df['ContractMonths'] >= 1]

# Check if 'ContractStatus' and 'MRR' columns exist in the DataFrame
if 'ContractStatus' not in customer_df.columns:
    customer_df['ContractStatus'] = 'Active'

if 'MRR' not in customer_df.columns:
    customer_df['MRR'] = 0

# Update contract status and MRR
customer_df[['ContractStatus', 'MRR']] = customer_df.apply(update_contract_status_and_mrr, axis=1)

# Calculate contract status
customer_df['ContractStatus'] = customer_df.apply(lambda row: calculate_contract_status(row['SnapshotDate'], row['FirstPurchaseDate']), axis=1)

# Save customer data to CSV files
customer_df.to_csv(os.path.join(data_dir, 'customer_detail_data.csv'), index=False)

# Create MRR data
mrr_data = customer_df[['SnapshotDate', 'MRR']].groupby('SnapshotDate').sum().reset_index()
mrr_data.to_csv(os.path.join(data_dir, 'mrr_data.csv'), index=False)

# Create support tickets data
support_tickets_data = customer_df[['SnapshotDate', 'SupportTickets']].groupby('SnapshotDate').sum().reset_index()
support_tickets_data.to_csv(os.path.join(data_dir, 'support_tickets_data.csv'), index=False)

# Create total customer base summary
total_customer_base_summary = customer_df.groupby('SnapshotDate')['CustomerID'].count().reset_index()
total_customer_base_summary.to_csv(os.path.join(data_dir, 'total_customer_base_summary.csv'), index=False)

# # Create new customers summary
# new_customers_summary = customer_df[customer_df['ContractStatus'] == 'Active'].groupby('SnapshotDate')['CustomerID'].count().reset_index()
# new_customers_summary.to_csv(os.path.join(data_dir, 'new_customers_summary.csv'), index=False)

# # Create combined summary
# combined_summary = pd.merge(total_customer_base_summary, mrr_data, on='SnapshotDate')
# combined_summary = pd.merge(combined_summary, support_tickets_data, on='SnapshotDate')
# combined_summary = pd.merge(combined_summary, new_customers_summary, on='SnapshotDate')
# combined_summary.to_csv(os.path.join(data_dir, 'combined_summary.csv'), index=False)
