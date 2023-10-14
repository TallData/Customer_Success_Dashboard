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
    first_names = ['Raphael','Richard','Thomas','Ahmed','Andre','Caden','Dallas','Eric','Ermias','Evan','Hayden','Ismael','Jamir','Jaylen','Kaden','Leon','Ava','Madison','Skylar','Riley','Amelia','Olivia','Zuri','Isabella','Fatoumata','Serenity','Zoey','Chloe','Aria','Fatima','Leah','Melody','Amina','Mariam','Nova','Aaliyah','Brielle','Layla','Mia','Grace','Nyla','Sophia','Aisha','Kylie','Miracle','Wynter','Autumn','Kayla','Kehlani','Reign','Savannah']
    last_names = ['SMITH','JOHNSON','WILLIAMS','BROWN','JONES','MILLER','DAVIS','GARCIA','RODRIGUEZ','WILSON','MARTINEZ','ANDERSON','TAYLOR','THOMAS','HERNANDEZ','MOORE','MARTIN','JACKSON','THOMPSON','WHITE','LOPEZ','LEE']
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return first_name, last_name

# Create a function to generate random purchase dates
def generate_purchase_date():
    return pd.to_datetime('2020-01-01') + pd.DateOffset(days=random.randint(0, 1200))

# Define the project directory
project_dir = "Customer_Success_Dashboard"

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
customers = pd.DataFrame({
    'CustomerID': [generate_customer_id() for _ in range(n_customers)],
    'Country': [random.choice(['USA', 'Canada', 'UK', 'Australia']) for _ in range(n_customers)],
    'State': [random.choice(['AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL',
        'GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MT','NE','NV','NH',
        'NJ','NM','NY','NC','ND','OH','OK','OR','MD','MA','MI','MN','MS','MO',
        'PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY',]) for _ in range(n_customers)],
    'Vertical': [np.random.choice(verticals, p=vertical_percentages) for _ in range(n_customers)]
})

# Generate monthly snapshots for a year
n_months = 12
snapshot_dates = pd.date_range(start='2022-01-01', periods=n_months, freq='M')

# Initialize lists to store data
customer_detail_data = []
mrr_data = []
support_tickets_data = []

# Generate customer detail data for each customer
for snapshot_date in snapshot_dates:
    for customer_id, customer_state in zip(customers['CustomerID'], customers['State']):
        first_name, last_name = generate_name()
        purchase_date = generate_purchase_date()
        assigned_vertical = customers.loc[customers['CustomerID'] == customer_id, 'Vertical'].values[0]  # Retrieve the assigned vertical
        
        # Filter out snapshot dates before the customer's FirstPurchaseDate
        if snapshot_date >= purchase_date:
            customer_detail_data.append({
                'SnapshotDate': snapshot_date,
                'CustomerID': customer_id,
                'FirstName': first_name,
                'LastName': last_name,
                'State': customer_state,  # Add the state to the data
                'FirstPurchaseDate': purchase_date, 
                'Vertical': assigned_vertical  # Add the assigned vertical
            })
            
            # Generate random MRR and support ticket data with 2 decimal places
            mrr = max(round(np.random.normal(1000, 250), -1),100)
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


# Create dataframes for customer detail, MRR, and support ticket data
customer_detail_data = pd.DataFrame(customer_detail_data)
mrr_data = pd.DataFrame(mrr_data)
support_tickets_data = pd.DataFrame(support_tickets_data)

# Generate MRR goals for each customer as a random value between 0.5 and 1.25 times the actual MRR
mrr_data['MRRGoal'] = round(mrr_data['MRR'] * random.uniform(0.3, 2), 2)
support_tickets_data['TotalCSAT'] = round(support_tickets_data['SupportTickets'] * support_tickets_data['AverageCSAT'],2)

# Save data to CSV in the data directory
customer_detail_file = os.path.join(data_dir, 'customer_detail_data.csv')
mrr_file = os.path.join(data_dir, 'mrr_data.csv')
support_tickets_file = os.path.join(data_dir, 'support_tickets_data.csv')

customer_detail_data.to_csv(customer_detail_file, index=False)
mrr_data.to_csv(mrr_file, index=False)
support_tickets_data.to_csv(support_tickets_file, index=False)

print("Mock customer success data generated and saved as CSV in the 'data' folder.")


# Merge customer_detail_data with mrr_data
combined_data = customer_detail_data.merge(mrr_data, on=['SnapshotDate', 'CustomerID'], how='left')

# Merge combined_data with support_tickets_data
combined_data = combined_data.merge(support_tickets_data, on=['SnapshotDate', 'CustomerID'], how='left')

# Save the combined data to a CSV file
combined_file = os.path.join(data_dir, 'combined_customer_data.csv')
combined_data.to_csv(combined_file, index=False)

print("Combined customer data saved as CSV in the 'data' folder.")

# Calculate MRR and Support Tickets summary for the total customer base
total_customer_base_summary = combined_data.groupby('SnapshotDate').agg({
    'MRR': 'sum',
    'SupportTickets': 'sum',
    'TotalCSAT': 'sum'
}).rename(columns={'MRR': 'Total_MRR', 'SupportTickets': 'Total_SupportTickets','TotalCSAT': 'TotalCSAT'}).reset_index()

# Calculate MRR and Support Tickets summary for new customers matching the purchase date and snapshot date
new_customers_summary = combined_data[combined_data['FirstPurchaseDate'] == combined_data['SnapshotDate']].groupby('SnapshotDate').agg({
    'MRR': 'sum',
    'SupportTickets': 'sum',
    'TotalCSAT': 'sum'
}).rename(columns={'MRR': 'New_MRR', 'SupportTickets': 'New_SupportTickets','TotalCSAT': 'New_TotalCSAT'}).reset_index()

# Save the summary data to CSV
total_customer_base_summary.to_csv(os.path.join(data_dir, 'total_customer_base_summary.csv'), index=False)
new_customers_summary.to_csv(os.path.join(data_dir, 'new_customers_summary.csv'), index=False)

print("SnapshotDate data psrts saved as CSV in the 'data' folder.")

# Combine total_customer_base_summary and new_customers_summary
combined_summary = total_customer_base_summary.merge(new_customers_summary, on='SnapshotDate', how='left')

# Save the combined summary data to CSV
combined_summary.to_csv(os.path.join(data_dir, 'combined_summary.csv'), index=False)

print("SnapshotDate combined data saved as CSV in the 'data' folder.")