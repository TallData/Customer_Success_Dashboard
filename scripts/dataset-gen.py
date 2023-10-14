import pandas as pd
import random
import string
import numpy as np
import os

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

# Create a function to generate random customer IDs
def generate_customer_id():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

# Generate customer demographics data
n_customers = 1000
customers = pd.DataFrame({
    'CustomerID': [generate_customer_id() for _ in range(n_customers)],
    'Country': [random.choice(['USA', 'Canada', 'UK', 'Australia']) for _ in range(n_customers)],
    'State': [random.choice(['NC', 'CA', 'TX', 'NY', 'FL']) for _ in range(n_customers)],
})

# Generate monthly snapshots for a year
n_months = 12
snapshot_dates = pd.date_range(start='2022-01-01', periods=n_months, freq='M')

# Initialize lists to store data
snapshot_data = []

# Generate data for each month
for snapshot_date in snapshot_dates:
    total_customers = random.randint(800, 1000)
    new_customers = random.randint(10, 50)
    upsell_customers = random.randint(5, 30)
    downgrade_customers = random.randint(0, 20)
    churn_customers = random.randint(5, 40)
    
    mrr_new = np.random.normal(2000, 200)
    mrr_upsell = np.random.normal(1500, 150)
    mrr_downgrade = np.random.normal(500, 50)
    mrr_churn = np.random.normal(1000, 100)
    
    arr_new = mrr_new * 12
    arr_upsell = mrr_upsell * 12
    arr_downgrade = mrr_downgrade * 12
    arr_churn = mrr_churn * 12
    
    support_tickets = random.randint(0, 100)
    average_ticket_score = round(random.uniform(3, 5), 2)
    unsatisfactory_tickets = random.randint(0, 10)
    
    snapshot_data.append({
        'SnapshotDate': snapshot_date,
        'TotalCustomers': total_customers,
        'NewCustomers': new_customers,
        'UpsellCustomers': upsell_customers,
        'DowngradeCustomers': downgrade_customers,
        'ChurnCustomers': churn_customers,
        'MRR_New': mrr_new,
        'MRR_Upsell': mrr_upsell,
        'MRR_Downgrade': mrr_downgrade,
        'MRR_Churn': mrr_churn,
        'ARR_New': arr_new,
        'ARR_Upsell': arr_upsell,
        'ARR_Downgrade': arr_downgrade,
        'ARR_Churn': arr_churn,
        'SupportTickets': support_tickets,
        'AverageTicketScore': average_ticket_score,
        'UnsatisfactoryTickets': unsatisfactory_tickets
    })

# Create a dataframe for snapshot summary data
snapshot_summary_data = pd.DataFrame(snapshot_data)

# Save snapshot summary data to CSV in the data directory
snapshot_summary_file = os.path.join(data_dir, 'snapshot_summary_data.csv')
snapshot_summary_data.to_csv(snapshot_summary_file, index=False)

print("Mock customer success summary data generated and saved as CSV in the 'data' folder.-"+data_dir)

# Create customer detail data with a row for each customer at each snapshot
customer_detail_data = []

for snapshot_date in snapshot_dates:
    for customer in customers['CustomerID']:
        customer_detail_data.append({
            'SnapshotDate': snapshot_date,
            'CustomerID': customer
        })

# Create a dataframe for customer detail data
customer_detail_data = pd.DataFrame(customer_detail_data)

# Save customer detail data to CSV in the data directory
customer_detail_file = os.path.join(data_dir, 'customer_detail_data.csv')
customer_detail_data.to_csv(customer_detail_file, index=False)

print("Mock customer success detail data generated and saved as CSV in the 'data' folder.")
