import pandas as pd
import matplotlib.pyplot as plt
import os

# Set the project directory
project_dir = "/Users/stak/dev/Customer_Success_Dashboard/"

# Set the data and analysis directories
data_dir = os.path.join(project_dir, "data")
analysis_dir = os.path.join(project_dir, "analysis")

#print(data_dir)

# Create the analysis directory if it doesn't exist
if not os.path.exists(analysis_dir):
    os.mkdir(analysis_dir)

# Load the combined customer data
combined_data = pd.read_csv(os.path.join(data_dir, 'customer_detail_data.csv'))

# Group the data by 'SnapshotDate' and 'Verticals', and calculate the mean MRR for each group
mrr_by_vertical = combined_data.groupby(['SnapshotDate', 'Vertical'])['MRR'].mean().reset_index()

# Pivot the data to create a pivot table for plotting
mrr_by_vertical_pivot = mrr_by_vertical.pivot(index='SnapshotDate', columns='Vertical', values='MRR')

# Plot the data
plt.figure(figsize=(12, 6))
for vertical in mrr_by_vertical_pivot.columns:
    plt.plot(mrr_by_vertical_pivot.index, mrr_by_vertical_pivot[vertical], label=vertical)

plt.title('Monthly Average MRR by Vertical')
plt.xlabel('Snapshot Date')
plt.ylabel('Average MRR')
plt.legend(loc='upper right')
plt.grid(True)

# Adjust x-axis labels
plt.xticks(rotation=45)  # Rotate labels by 45 degrees

# Save the plot in the analysis folder
plot_file = os.path.join(analysis_dir, 'monthly_mrr_by_vertical.png')
plt.savefig(plot_file)

# Display a message indicating the successful generation of the plot
print(f"Monthly MRR by Vertical plot saved as {plot_file}")

# Display the plot
#plt.show()
