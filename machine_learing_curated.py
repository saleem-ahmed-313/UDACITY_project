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

# Script generated for node steptrainer_trusted
steptrainer_trusted_node1745314537862 = glueContext.create_dynamic_frame.from_catalog(database="finaldatabase", table_name="steptrainer_trusted", transformation_ctx="steptrainer_trusted_node1745314537862")

# Script generated for node accelerometer_trusted
accelerometer_trusted_node1745314562737 = glueContext.create_dynamic_frame.from_catalog(database="finaldatabase", table_name="accelerometer_trusted", transformation_ctx="accelerometer_trusted_node1745314562737")

# Script generated for node Join
Join_node1745314589281 = Join.apply(frame1=steptrainer_trusted_node1745314537862, frame2=accelerometer_trusted_node1745314562737, keys1=["sensorreadingtime"], keys2=["timestamp"], transformation_ctx="Join_node1745314589281")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=Join_node1745314589281, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1745314496747", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1745314690522 = glueContext.getSink(path="s3://finalprojectsaleem/machine_learning_curated/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1745314690522")
AmazonS3_node1745314690522.setCatalogInfo(catalogDatabase="finaldatabase",catalogTableName="machine_learning_curated")
AmazonS3_node1745314690522.setFormat("json")
AmazonS3_node1745314690522.writeFrame(Join_node1745314589281)
job.commit()
