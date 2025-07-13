import pandas as pd

def generate_sql_constraints(input_csv, output_sql):
    """
    Reads candidate foreign key relationships from a CSV file,
    generates ALTER TABLE SQL statements for each valid candidate,
    and writes them to an output SQL file.
    """
    # Define a function to generate a safe constraint name
    def get_constraint_name(referencing_table, referencing_column, referenced_table, referenced_column):
        return f"fk_{referencing_table}_{referencing_column}_{referenced_table}_{referenced_column}"

    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv)

    # Open the output file in write mode
    with open(output_sql, 'w') as f:
        # Iterate over each row in the DataFrame
        for index, row in df.iterrows():
            # Extract the values from the row
            referencing_table = row['referencing_table']
            referencing_column = row['referencing_column']
            referenced_table = row['referenced_table']
            referenced_column = row['referenced_column']

            # Generate the constraint name
            constraint_name = get_constraint_name(referencing_table, referencing_column, referenced_table, referenced_column)

            # Generate the ALTER TABLE SQL statement
            sql_statement = f"ALTER TABLE {referencing_table} ADD CONSTRAINT {constraint_name} FOREIGN KEY ({referencing_column}) REFERENCES {referenced_table}({referenced_column});"

            # Write the SQL statement to the output file
            f.write(sql_statement + '\n')

if __name__ == "__main__":
    generate_sql_constraints('fk_candidates.csv', 'suggested_constraints.sql')
