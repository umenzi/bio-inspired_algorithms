import pandas as pd
import ast

# Set the display options to show all rows and columns and no width limit
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Read the CSV file
df = pd.read_csv('../results.csv')

# Create a list with the new index values
new_index = ['aco' if i == 1 else 'adpe_aco' if i == 2 else 'pso' if i == 3 else 'firefly' if i == 4 else '' for i in df.index]

# Set the new index
df.index = new_index


# We round every value to 2 decimals
def round_tuple(t):
    return tuple(round(float(x), 2) for x in t)


# Store the headers
headers = df.columns

# Apply the function to each cell in the DataFrame, excluding the headers
df = df.applymap(lambda x: round_tuple(ast.literal_eval(x)) if isinstance(x, str) and x.startswith('(') else x)

# Reassign the headers
df.columns = headers

# Print the resulting data table
print(df)
