from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_CENTER
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import os

# Set the project directory
project_dir = "Customer_Success_Dashboard"

# Set the data and report directories
data_dir = os.path.join(project_dir, "data")
report_dir = os.path.join(project_dir, "report")

# Create the report directory if it doesn't exist
if not os.path.exists(report_dir):
    os.mkdir(report_dir)

# Load the combined customer data
combined_data = pd.read_csv(os.path.join(data_dir, 'combined_customer_data.csv'))

# Group the data by 'SnapshotDate' and 'Verticals', and calculate the mean MRR for each group
mrr_by_vertical = combined_data.groupby(['SnapshotDate', 'Vertical'])['MRR'].mean().reset_index()

# Convert 'SnapshotDate' to a formatted date
mrr_by_vertical['SnapshotDate'] = pd.to_datetime(mrr_by_vertical['SnapshotDate'])
mrr_by_vertical['SnapshotDate'] = mrr_by_vertical['SnapshotDate'].dt.strftime('%m-%y')

# Plot the data for monthly average MRR by vertical
plt.figure(figsize=(8, 4))
for vertical in mrr_by_vertical['Vertical'].unique():
    vertical_data = mrr_by_vertical[mrr_by_vertical['Vertical'] == vertical]
    plt.plot(vertical_data['SnapshotDate'], vertical_data['MRR'], label=vertical)

plt.title('Monthly Average MRR by Vertical')
plt.xlabel('Snapshot Date')
plt.ylabel('Average MRR')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.grid(True)

# Save the plot in the report directory
plot_file = os.path.join(report_dir, 'monthly_mrr_by_vertical.png')
plt.savefig(plot_file)

# Create a PDF report
doc = SimpleDocTemplate(os.path.join(report_dir, 'dashboard_report.pdf'), pagesize=letter)
story = []

# Add a title to the report
title_style = getSampleStyleSheet()["Title"]
title_style.alignment = TA_CENTER
story.append(Paragraph("Customer Success Dashboard Report", title_style))

# Add a section for MRR by vertical
section_style = getSampleStyleSheet()["Heading1"]
section_style.alignment = TA_CENTER
story.append(Paragraph("Monthly Average MRR by Vertical", section_style))
story.append(Image(plot_file, width=400, height=200))
summary_text_mrr = "The plot shows the monthly average MRR by vertical. It provides insights into the performance of each vertical over time."
story.append(Paragraph(summary_text_mrr, style=ParagraphStyle(name='SummaryStyle', fontSize=12, alignment=TA_CENTER)))

# Add a section for Percentage of MRR to Goal
story.append(Paragraph("Monthly Percentage of MRR to Goal by Vertical (Smoothed)", section_style))
pct_goal_plot_file = os.path.join(report_dir, 'monthly_pct_to_goal_by_vertical.png')
plt.savefig(pct_goal_plot_file)
story.append(Image(pct_goal_plot_file, width=400, height=200))
summary_text_pct_goal = "This plot represents the percentage of achieved MRR compared to the MRR goal, smoothed over time. It shows the performance of each vertical in reaching their goals."
story.append(Paragraph(summary_text_pct_goal, style=ParagraphStyle(name='SummaryStyle', fontSize=12, alignment=TA_CENTER)))

# Add a section for Support Tickets per Account by Vertical
support_tickets_by_vertical = combined_data.groupby(['SnapshotDate', 'Vertical'])['SupportTickets'].mean().reset_index()
support_tickets_by_vertical['SnapshotDate'] = pd.to_datetime(support_tickets_by_vertical['SnapshotDate'])
support_tickets_by_vertical['SnapshotDate'] = support_tickets_by_vertical['SnapshotDate'].dt.strftime('%m-%y')
story.append(Paragraph("Support Tickets per Account by Vertical", section_style))
support_tickets_plot_file = os.path.join(report_dir, 'support_tickets_by_vertical.png')

# Plot the data for support tickets by vertical
plt.figure(figsize=(8, 4))
for vertical in support_tickets_by_vertical['Vertical'].unique():
    vertical_data = support_tickets_by_vertical[support_tickets_by_vertical['Vertical'] == vertical]
    plt.plot(vertical_data['SnapshotDate'], vertical_data['SupportTickets'], label=vertical)

plt.title('Support Tickets per Account by Vertical')
plt.xlabel('Snapshot Date')
plt.ylabel('Average Support Tickets')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.grid(True)

# Save the support tickets plot
plt.savefig(support_tickets_plot_file)
story.append(Image(support_tickets_plot_file, width=400, height=200))
summary_text_support_tickets = "This plot displays the average number of support tickets per account by vertical. It highlights the support ticket performance across different verticals."
story.append(Paragraph(summary_text_support_tickets, style=ParagraphStyle(name='SummaryStyle', fontSize=12, alignment=TA_CENTER)))

# Build the PDF report
doc.build(story)

# Display a message indicating the successful generation of the report
print(f"Customer Success Dashboard Report saved as {os.path.join(report_dir, 'dashboard_report.pdf')}")
