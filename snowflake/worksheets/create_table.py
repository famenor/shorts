# The Snowpark package is required for Python Worksheets. 
# You can add more packages by selecting them using the Packages control and then importing them.

import snowflake.snowpark as snowpark
from snowflake.snowpark.functions import col

def main(session: snowpark.Session): 

  tableName = "anuncios_db.bronce.range_table"
  df_range = session.range(1, 10, 2).to_df('a')
  df_range.write.mode("overwrite").save_as_table(tableName)
  return tableName + " table successfully created"