import os

# Define the project directory
project_dir = "Customer_Success_Dashboard"

# Define subdirectories
directories = [
    "data",
    "analysis",
    "reports",
    "visualizations",
    "scripts",
]

# Create the project directory if it doesn't exist
if not os.path.exists(project_dir):
    os.mkdir(project_dir)

# Create subdirectories
for directory in directories:
    dir_path = os.path.join(project_dir, directory)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

print("Project folder structure created.")
