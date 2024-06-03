import pandas as pd
from sqlalchemy import create_engine
from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P

# Database setup
DATABASE_URI = 'postgresql://postgres:postgres@localhost/school_management'
engine = create_engine(DATABASE_URI)

# Define the path to the ODS file
file_path = '/home/kokonya/Documents/2024_Spark_expenses.ods'

# Load the ODS file
doc = load(file_path)

# Extract data from the ODS file
data = []
for table in doc.getElementsByType(Table):
    for row in table.getElementsByType(TableRow):
        row_data = []
        for cell in row.getElementsByType(TableCell):
            # Extract the text content from the cell
            cell_value = ""
            for p in cell.getElementsByType(P):
                for node in p.childNodes:
                    if node.nodeType == node.TEXT_NODE:
                        cell_value += node.data
            row_data.append(cell_value)
        data.append(row_data)

# Extract the column headers from the third row
columns = data[2]  # Third row (index 2) contains the column headers

# Extract the data starting from the fourth row
data_rows = data[3:]  # Data starts from the fourth row (index 3)

# Convert the extracted data to a DataFrame
df = pd.DataFrame(data_rows, columns=columns)

# Ensure correct data types
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

# Drop any rows where 'date' or 'amount' could not be parsed
df = df.dropna(subset=['date', 'amount'])

# Insert data into the expenditures table
df.to_sql('expenditures', con=engine, if_exists='append', index=False)

print("Data inserted successfully!")
