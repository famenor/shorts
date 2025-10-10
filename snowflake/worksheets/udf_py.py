import snowflake.snowpark as snowpark

from snowflake.snowpark.functions import col
from snowflake.snowpark.types import IntegerType
from snowflake.snowpark.functions import udf, udtf, table_function
from snowflake.snowpark.types import StructField, StructType, StringType, IntegerType, FloatType

schema_01 = StructType([
  StructField("tipo", StringType()),
  StructField("ppm2", IntegerType()),
])

class PPM2:
    def process(self, tipo, costo, superficie):
        result = costo / superficie
        yield (tipo, result)

def main(session: snowpark.Session):

    #UDF
    add_one = udf(lambda x: x+1, return_type=IntegerType(), input_types=[IntegerType()])

    @udf(name="minus_one", is_permanent=True, stage_location="@anuncios_db.bronce.func_minus_one_stage", replace=True)
    def minus_one(x: int) -> int:
        return x - 1
    
    df_table = session.table("anuncios_db.bronce.anuncios")

    df_table = df_table.with_column('costo_p', add_one(col('costo')))
    df_table = df_table.with_column('costo_m', minus_one(col('costo')))

    #ppm2_obj = udtf(PPM2, output_schema=schema_01, input_types=[StringType(), IntegerType(), IntegerType()])

    #ppm2_df = session.table_function(ppm2_obj, df_table.select('tipo'), df_table.select('costo'), df_table.select('superficie')).collect()
      
    return df_table
    #return ppm2_df