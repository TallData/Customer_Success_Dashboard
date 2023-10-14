# Customer Success Dashboard

## Project Overview

This Python project generates mock data for a Customer Success Dashboard. It simulates customer demographics, monthly snapshots, MRR (Monthly Recurring Revenue), support tickets, and other relevant data for analysis. The goal is to provide a foundation for building a Customer Success Dashboard, which can help track and analyze customer performance and satisfaction.

## Project Structure

The project is organized into several code files:

1. **dataset-gen.py**: This script generates mock customer data, including customer details, MRR, and support tickets. It also calculates summary data for the total customer base and new customers, along with MRR goals for each customer.

2. **data**: This folder contains the generated data files in CSV format, including `customer_detail_data.csv`, `mrr_data.csv`, `support_tickets_data.csv`, `total_customer_base_summary.csv`, `new_customers_summary.csv`, and `combined_summary.csv`.

## Libraries Used

The project relies on several Python libraries for data generation, analysis, and manipulation:

- **Pandas**: Used for creating and managing dataframes, reading and writing CSV files, and performing data transformations.
- **Random**: Employed for generating random values, such as customer demographics, purchase dates, MRR, and support tickets.
- **String**: Used to generate random customer IDs.
- **NumPy**: Provides functions for generating random numbers and calculations.
- **os**: Utilized for handling directories and file operations.

## Running the Project

To run the project and generate mock data, execute the `dataset-gen.py` script. The generated data will be stored in the 'data' folder in CSV format.

## Customization
You can customize the project by adjusting parameters in the dataset-gen.py script. For instance, you can modify the number of customers, date ranges, and data distribution to better match your specific use case.
Example:

```shell
python dataset-gen.py
