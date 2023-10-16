import pandas as pd
import random
import string
import numpy as np
import os

random.seed(a=12345, version=2)

# Create a function to generate random customer IDs
def generate_customer_id():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

# Create a function to generate random first and last names
def generate_name():
    first_names = ['Raphael', 'Richard', 'Thomas', 'Ahmed', 'Andre', 'Caden', 'Dallas', 'Eric', 'Ermias', 'Evan', 'Hayden', 'Ismael', 'Jamir', 'Jaylen', 'Kaden', 'Leon', 'Ava', 'Madison', 'Skylar', 'Riley', 'Amelia', 'Olivia', 'Zuri', 'Isabella', 'Fatoumata', 'Serenity', 'Zoey', 'Chloe', 'Aria', 'Fatima', 'Leah', 'Melody', 'Amina', 'Mariam', 'Nova', 'Aaliyah', 'Brielle', 'Layla', 'Mia', 'Grace', 'Nyla', 'Sophia', 'Aisha', 'Kylie', 'Miracle', 'Wynter', 'Autumn', 'Kayla', 'Kehlani', 'Reign', 'Savannah']
    last_names = ['SMITH', 'JOHNSON', 'WILLIAMS', 'BROWN', 'JONES', 'MILLER', 'DAVIS', 'GARCIA', 'RODRIGUEZ', 'WILSON', 'MARTINEZ', 'ANDERSON', 'TAYLOR', 'THOMAS', 'HERNANDEZ', 'MOORE', 'MARTIN', 'JACKSON', 'THOMPSON', 'WHITE', 'LOPEZ', 'LEE']
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return first_name, last_name

# Create a function to generate random purchase dates
def generate_purchase_date():
    return pd.to_datetime('2020-01-01') + pd.DateOffset(days=random.randint(0, 1200))

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

# Function to update contract status and MRR
def update_contract_status_and_mrr(row):
    # Extract the current contract status and MRR
    contract_status = row['ContractStatus']
    current_mrr = row['MRR']

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

# Define the project directory
project_dir = "/Users/stak/dev/Customer_Success_Dashboard"

# Define the data directory
data_dir = os.path.join(project_dir, "data")

# Create the project directory if it doesn't exist
if not os.path.exists(project_dir):
    os.mkdir(project_dir)

# Create the data directory if it doesn't exist
if not os.path.exists(data_dir):
    os.mkdir(data_dir)

# Define the verticals and their corresponding percentages
verticals = ['Consultants', 'Non-Profit', 'Entertainment', 'Restaurants', 'Travel']
vertical_percentages = [0.30, 0.20, 0.10, 0.25, 0.15]

# Generate customer demographics data
n_customers = 10000

# Initialize lists to store customer demographic data
customers = []

# Generate customer detail data for each customer
for _ in range(n_customers):
    first_name, last_name = generate_name()
    purchase_date = generate_purchase_date()

    customer_data = {
        'CustomerID': generate_customer_id(),
        'Country': random.choice(['USA', 'Canada', 'UK', 'Australia']),
        'State': random.choice(['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL',
            'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MT', 'NE', 'NV', 'NH',
            'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO',
            'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', ]),
        'Vertical': np.random.choice(verticals, p=vertical_percentages),
        'FirstName': first_name,
        'LastName': last_name,
        'FirstPurchaseDate': generate_purchase_date()
    }

    customers.append(customer_data)

# Create a DataFrame for customer demographics
customers = pd.DataFrame(customers)
customer_file = os.path.join(data_dir, 'customer_file.csv')
customers.to_csv(customer_file, index=False)

# print("Mock customer data demo generated and saved as CSV in the 'data' folder.")

# Generate monthly snapshots for a year
n_months = 36
snapshot_dates = pd.date_range(start='2020-01-01', periods=n_months, freq='M')

# Initialize lists to store data
customer_detail_data = []
mrr_data = []
support_tickets_data = []

# Generate customer detail data for each customer
for snapshot_date in snapshot_dates:
    for _, customer in customers.iterrows():
        customer_id = customer['CustomerID']
        customer_state = customer['State']
        assigned_vertical = customer['Vertical']

        # Filter out snapshot dates before the customer's FirstPurchaseDate
        if snapshot_date >= customer['FirstPurchaseDate']:
            contract_months = ((snapshot_date - customer['FirstPurchaseDate']).days // 30 % 12) + 1
            contract_status = simulate_churn_upsell({
                'SnapshotDate': snapshot_date,
                'FirstPurchaseDate': customer['FirstPurchaseDate']
            })

            # Create a dictionary with the relevant customer data
            customer_data = {
                'SnapshotDate': snapshot_date,
                'CustomerID': customer_id,
                'FirstName': customer['FirstName'],
                'LastName': customer['LastName'],
                'State': customer_state,
                'FirstPurchaseDate': customer['FirstPurchaseDate'],
                'Vertical': assigned_vertical,
                'ContractMonth': contract_months,
                'ContractStatus': contract_status
            }

            # Apply the 'update_contract_status_and_mrr' function to update ContractStatus and MRR
            updated_data = update_contract_status_and_mrr(customer_data)

            # Append the updated data to the customer_detail_data list
            customer_detail_data.append(updated_data)

            # Generate random MRR and support ticket data with 2 decimal places
            mrr = max(round(np.random.normal(1000, 550), -1), 100)
            support_tickets = random.randint(0, 10)
            average_ticket_score = round(random.uniform(0, 5), 2)

            mrr_data.append({
                'SnapshotDate': snapshot_date,
                'CustomerID': customer_id,
                'MRR': mrr
            })

            support_tickets_data.append({
                'SnapshotDate': snapshot_date,
                'CustomerID': customer_id,
                'SupportTickets': support_tickets,
                'AverageCSAT': average_ticket_score
            })

# # Create dataframes for customer detail, MRR, and support ticket data
# customer_detail_data = pd.DataFrame(customer_detail_data)
# mrr_data = pd.DataFrame(mrr_data)
# support_tickets_data = pd.DataFrame(support_tickets_data)

# support_tickets_data['TotalCSAT'] = round(support_tickets_data['SupportTickets'] * support_tickets_data['AverageCSAT'],2)

# # Merge 'mrr_data' into 'customer_detail_data'
# combined_data = customer_detail_data.merge(mrr_data, on=['CustomerID', 'SnapshotDate'], how='left')
# combined_data = combined_data.merge(support_tickets_data, on=['CustomerID', 'SnapshotDate'], how='left')

# # Apply the update_contract_status_and_mrr function to update the data
# combined_data[['ContractStatus', 'MRR']] = combined_data.apply(update_contract_status_and_mrr, axis=1)

# # Identify the first churn date for each customer
# first_churn_dates = combined_data[combined_data['ContractStatus'] == 'Churned'].groupby('CustomerID')['SnapshotDate'].min().reset_index()

# # Merge this information back into the customer_detail_data
# combined_data = combined_data.merge(first_churn_dates, on='CustomerID', suffixes=('', '_FirstChurn'))

# # Filter out records with a SnapshotDate later than the first churn date
# combined_data = combined_data[combined_data['SnapshotDate'] <= combined_data['SnapshotDate_FirstChurn']]

# # Clean up by removing unnecessary columns
# combined_data.drop(columns=['SnapshotDate_FirstChurn'], inplace=True)

# # Save data to CSV in the data directory
# combined_customer_file = os.path.join(data_dir, 'combined_customer_data.csv')
# mrr_data.to_csv(os.path.join(data_dir, 'mrr_data.csv'), index=False)
# support_tickets_data.to_csv(os.path.join(data_dir, 'support_tickets_data.csv'), index=False)

# print("Mock customer success detail for MRR, Support Tickets, and Customer Demo is generated and saved as CSV in the 'data' folder.")


# combined_data.to_csv(combined_customer_file, index=False)

# print("Mock combined data generated and saved as CSV in the 'data' folder.")

# # Calculate MRR and Support Tickets summary for the total customer base
# total_customer_base_summary = combined_data.groupby('SnapshotDate').agg({
#     'MRR': 'sum',
#     'SupportTickets': 'sum',
#     'TotalCSAT': 'sum'
# }).rename(columns={'MRR': 'Total_MRR', 'SupportTickets': 'Total_SupportTickets','TotalCSAT': 'TotalCSAT'}).reset_index()

# # Calculate MRR and Support Tickets summary for new customers matching the purchase date and snapshot date
# new_customers_summary = combined_data[combined_data['FirstPurchaseDate'] == combined_data['SnapshotDate']].groupby('SnapshotDate').agg({
#     'MRR': 'sum',
#     'SupportTickets': 'sum',
#     'TotalCSAT': 'sum'
# }).rename(columns={'MRR': 'New_MRR', 'SupportTickets': 'New_SupportTickets','TotalCSAT': 'New_TotalCSAT'}).reset_index()

# # Save the summary data to CSV
# total_customer_base_summary.to_csv(os.path.join(data_dir, 'total_customer_base_summary.csv'), index=False)
# new_customers_summary.to_csv(os.path.join(data_dir, 'new_customers_summary.csv'), index=False)

# print("SnapshotDate summary parts saved as CSV in the 'data' folder.")

# # Combine total_customer_base_summary and new_customers_summary
# combined_summary = total_customer_base_summary.merge(new_customers_summary, on='SnapshotDate', how='left')

# # Save the combined summary data to CSV
# combined_summary.to_csv(os.path.join(data_dir, 'combined_summary.csv'), index=False)

# print("New customer summary parts saved as CSV in the 'data' folder.")