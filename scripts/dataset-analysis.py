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
print(data_dir)

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


combined_data.to_csv(os.path.join(data_dir, 'analysis_test.csv'), index=False)

#Add a new column 'MRR_PercentToGoal' by dividing 'MRR' by 'PercentToGoal'
combined_data['MRR_PercentToGoal'] = combined_data['MRR'] / combined_data['PercentToGoal']

# Group the data by 'Vertical' and calculate the mean MRR and MRR_PercentToGoal for each group
mrr_by_vertical = combined_data.groupby('Vertical')[['MRR', 'MRR_PercentToGoal']].mean()

# Plot the data as side-by-side bar charts
plt.figure(figsize=(12, 6))
mrr_by_vertical.plot(kind='bar', width=0.4)
plt.title('Monthly Average MRR and MRR Percent to Goal by Vertical')
plt.xlabel('Vertical')
plt.ylabel('Average MRR')
plt.legend(['MRR', 'MRR Percent to Goal'])
plt.grid(True)

# Set the Y-axis limits
plt.ylim(1000, 2000)

# Rotate the X-axis labels by 0 degrees
plt.xticks(rotation=0)

# Save the plot in the analysis folder
plot_file = os.path.join(analysis_dir, 'monthly_mrr_vs_mrr_percent_to_goal_by_vertical.png')
plt.savefig(plot_file)

# Display a message indicating the successful generation of the plot
print(f"Monthly MRR vs MRR Percent to Goal by Vertical plot saved as {plot_file}")

# # Display the plot
# #plt.show()
