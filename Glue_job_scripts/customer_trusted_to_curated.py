import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue import DynamicFrame

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node accelerometer_trusted
accelerometer_trusted_node1745312916301 = glueContext.create_dynamic_frame.from_catalog(database="finaldatabase", table_name="accelerometer_trusted", transformation_ctx="accelerometer_trusted_node1745312916301")

# Script generated for node customer_trusted
customer_trusted_node1745312877151 = glueContext.create_dynamic_frame.from_catalog(database="finaldatabase", table_name="customer_trusted", transformation_ctx="customer_trusted_node1745312877151")

# Script generated for node SQL Query
SqlQuery0 = '''
select distinct c.customername,
c.email,
c.phone,
c.birthday,
c.serialnumber,
c.registrationdate,
c.lastupdatedate,
c.sharewithresearchasofdate,
c.sharewithpublicasofdate,
c.sharewithfriendsasofdate
from customer c 
join accelerometer a
on c.email = a.user
'''
SQLQuery_node1745312941520 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"customer":customer_trusted_node1745312877151, "accelerometer":accelerometer_trusted_node1745312916301}, transformation_ctx = "SQLQuery_node1745312941520")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=SQLQuery_node1745312941520, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1745313424599", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1745313462883 = glueContext.getSink(path="s3://finalprojectsaleem/customer/curated/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1745313462883")
AmazonS3_node1745313462883.setCatalogInfo(catalogDatabase="finaldatabase",catalogTableName="customer_curated")
AmazonS3_node1745313462883.setFormat("json")
AmazonS3_node1745313462883.writeFrame(SQLQuery_node1745312941520)
job.commit()
