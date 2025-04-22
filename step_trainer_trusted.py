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

# Script generated for node customer_curated
customer_curated_node1745313758346 = glueContext.create_dynamic_frame.from_catalog(database="finaldatabase", table_name="customer_curated", transformation_ctx="customer_curated_node1745313758346")

# Script generated for node steptrainer
steptrainer_node1745313734418 = glueContext.create_dynamic_frame.from_catalog(database="finaldatabase", table_name="steptrainer_landing", transformation_ctx="steptrainer_node1745313734418")

# Script generated for node SQL Query
SqlQuery0 = '''
select distinct s.sensorreadingtime,
s.serialnumber,s.distancefromobject
from steptrainer s 
inner join customer_curated c
on s.serialnumber = c.serialnumber


'''
SQLQuery_node1745314070251 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"steptrainer":steptrainer_node1745313734418, "customer_curated":customer_curated_node1745313758346}, transformation_ctx = "SQLQuery_node1745314070251")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=SQLQuery_node1745314070251, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1745313648135", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1745314302198 = glueContext.getSink(path="s3://finalprojectsaleem/step_trainer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1745314302198")
AmazonS3_node1745314302198.setCatalogInfo(catalogDatabase="finaldatabase",catalogTableName="steptrainer_trusted")
AmazonS3_node1745314302198.setFormat("json")
AmazonS3_node1745314302198.writeFrame(SQLQuery_node1745314070251)
job.commit()
