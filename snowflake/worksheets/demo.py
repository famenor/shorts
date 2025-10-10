# The Snowpark package is required for Python Worksheets. 
# You can add more packages by selecting them using the Packages control and then importing them.

import snowflake.snowpark as snowpark
from snowflake.snowpark.functions import col

def main(session: snowpark.Session, tipo: str): 
    # Your code goes here, inside the "main" handler.
    tableName = 'anuncios'
    dataframe = session.table(tableName).filter(col("tipo") == tipo)

    # Print a sample of the dataframe to standard output.
    dataframe.show()

    # Return value will appear in the Results tab.
    return dataframe

def execute_main(session: snowpark.Session):
    df = main(session, 'casa')
    return df