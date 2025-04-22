import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality

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

# Script generated for node CustomertrustedData
CustomertrustedData_node1745301464483 = glueContext.create_dynamic_frame.from_catalog(database="finaldatabase", table_name="customer_trusted", transformation_ctx="CustomertrustedData_node1745301464483")

# Script generated for node AccelerometerData
AccelerometerData_node1745301165475 = glueContext.create_dynamic_frame.from_catalog(database="finaldatabase", table_name="accelerometer_landing", transformation_ctx="AccelerometerData_node1745301165475")

# Script generated for node Join
Join_node1745301213533 = Join.apply(frame1=AccelerometerData_node1745301165475, frame2=CustomertrustedData_node1745301464483, keys1=["user"], keys2=["email"], transformation_ctx="Join_node1745301213533")

# Script generated for node Select Fields
SelectFields_node1745301261258 = SelectFields.apply(frame=Join_node1745301213533, paths=["z", "user", "y", "x", "timestamp"], transformation_ctx="SelectFields_node1745301261258")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=SelectFields_node1745301261258, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1745300140421", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1745301294820 = glueContext.getSink(path="s3://finalprojectsaleem/accelerometer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1745301294820")
AmazonS3_node1745301294820.setCatalogInfo(catalogDatabase="finaldatabase",catalogTableName="accelerometer_trusted")
AmazonS3_node1745301294820.setFormat("json")
AmazonS3_node1745301294820.writeFrame(SelectFields_node1745301261258)
job.commit()
