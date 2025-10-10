--CREATE DATABASE AND DATAWAREHOUSE
USE DATABASE ANUNCIOS_DB
CREATE SCHEMA bronce

CREATE WAREHOUSE anuncios_dw WITH
   WAREHOUSE_SIZE='X-SMALL'
   AUTO_SUSPEND = 180
   AUTO_RESUME = TRUE
   INITIALLY_SUSPENDED=TRUE;

SELECT CURRENT_WAREHOUSE()

SHOW USERS;

--STAGES
CREATE OR REPLACE STAGE anuncios_db.bronce.blob_stage
url = 's3://sfquickstarts/tastybytes/'
file_format = (type = csv);

CREATE OR REPLACE TABLE anuncios_db.bronce.menu
(
    menu_id NUMBER(19,0),
    menu_type_id NUMBER(38,0),
    menu_type VARCHAR(16777216),
    truck_brand_name VARCHAR(16777216),
    menu_item_id NUMBER(38,0),
    menu_item_name VARCHAR(16777216),
    item_category VARCHAR(16777216),
    item_subcategory VARCHAR(16777216),
    cost_of_goods_usd NUMBER(38,4),
    sale_price_usd NUMBER(38,4),
    menu_item_health_metrics_obj VARIANT
);

COPY INTO anuncios_db.bronce.menu
FROM @anuncios_db.bronce.blob_stage/raw_pos/menu/;

SELECT * FROM anuncios_db.bronce.menu LIMIT 20

SHOW STAGES
SHOW INTEGRATIONS
SHOW FILE FORMATS

-- INGEST VIA STAGE
LIST @DIM_HORA_STAGE;

CREATE OR REPLACE TABLE anuncios_db.bronce.dim_horas
(
    id NUMBER(5,0),
    grupo NUMBER(5,0),
    descripcion VARCHAR(255),
    hora NUMBER(5,0)
);

SELECT * FROM anuncios_db.bronce.dim_horas

-- JSON
CREATE TABLE anuncios_db.bronce.raw_source (SRC VARIANT);

CREATE STAGE json_stage URL = 's3://snowflake-docs/tutorials/json';
LIST @JSON_STAGE

COPY INTO anuncios_db.bronce.raw_source
  FROM @JSON_STAGE/server/2.6/2016/07/15/15
  FILE_FORMAT = (TYPE = JSON);

SELECT * FROM anuncios_db.bronce.raw_source

SELECT src:device_type::string AS device_type FROM anuncios_db.bronce.raw_source;

SELECT value:f::number FROM anuncios_db.bronce.raw_source, LATERAL FLATTEN( INPUT => SRC:events );

SELECT src:device_type::string, src:version::String, VALUE
FROM anuncios_db.bronce.raw_source, LATERAL FLATTEN( INPUT => SRC:events );

CREATE TABLE anuncios_db.bronce.flattened_source AS
  SELECT
    src:device_type::string AS device_type,
    src:version::string     AS version,
    VALUE                   AS src
  FROM
    anuncios_db.bronce.raw_source,
    LATERAL FLATTEN( INPUT => SRC:events );

SELECT * FROM anuncios_db.bronce.flattened_source

CREATE TABLE anuncios_db.bronce.events AS
  SELECT
    src:device_type::string                             as device_type
  , src:version::string                                 as version
  , value:f::number                                     as f
  , value:rv::variant                                   as rv
  , value:t::number                                     as t
  , value:v.ACHZ::number                                as achz
  , value:v.ACV::number                                 as acv
  , value:v.DCA::number                                 as dca
  , value:v.DCV::number                                 as dcv
  , value:v.ENJR::number                                as enjr
  , value:v.ERRS::number                                as errs
  , value:v.MXEC::number                                as mxec
  , value:v.TMPI::number                                as tmpi
  , value:vd::number                                    as vd
  , value:z::number                                     as z
  FROM
    anuncios_db.bronce.raw_source
  , lateral flatten ( input => SRC:events );

  SELECT * FROM anuncios_db.bronce.events

  -- UDF

  CREATE STAGE anuncios_db.bronce.func_minus_one_stage
  SHOW STAGES


-- TAGS

CREATE TAG madurez ALLOWED_VALUES 'bronce', 'plata', 'oro'
CREATE TAG tipo ALLOWED_VALUES 'hecho', 'dimension'


ALTER TABLE anuncios_db.bronce.anuncios SET TAG madurez='bronce', tipo='hecho'
ALTER TABLE anuncios_db.bronce.dim_horas SET TAG madurez='bronce', tipo='dimension'

SELECT * FROM TABLE(anuncios_db.INFORMATION_SCHEMA.TAG_REFERENCES('bronce.anuncios', 'table'));

SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.TAG_REFERENCES
    WHERE TAG_NAME = 'madurez'
    ORDER BY OBJECT_DATABASE, OBJECT_SCHEMA, OBJECT_NAME, COLUMN_NAME;

SELECT * FROM TABLE(anuncios_db.INFORMATION_SCHEMA.TAG_REFERENCES_ALL_COLUMNS('anuncios_db.bronce.anuncios', 'table'))
