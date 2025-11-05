# 🌊 IoT Data Lake Curation on AWS Glue

[![Project Stage](https://img.shields.io/badge/Status-Complete-success)]()
[![Tech Stack](https://img.shields.io/badge/Platform-AWS_Glue_%26_S3-orange?logo=amazon-aws)]()
[![Data Focus](https://img.shields.io/badge/Data-IoT_Telemetry-blue)]()

---

## 🎯 Project Goal

The main objective of this project was to build a simple, serverless **Data Lake** on AWS (using **S3** and **Glue**) to process raw **IoT device data** (Accelerometer, Step Trainer) and **Customer records**.

We needed to clean up and combine this data to create a high-quality dataset specifically for a **Machine Learning (ML)** team.

The pipeline ensures we only use data from customers who have explicitly agreed to share their information.

---

## 🏗️ Data Lake Architecture & Flow

We followed the standard Data Lake practice of dividing our S3 storage into three key zones.

| Zone | Purpose | Key Action |
| :--- | :--- | :--- |
| **Landing** | Stores raw, untouched data (initial upload). | Define schemas (e.g., `customer_landing`). |
| **Trusted** | Contains clean, filtered, and quality-checked data. | Filter out non-consenting customers (`step_trainer_trusted`). |
| **Curated** | Final, aggregated, and optimized data ready for analysis/ML. | Combine different data sources for ML (`machine_learning_curated`). |

### **The Three Main ETL Steps (AWS Glue Jobs)**

These jobs transform the data progressively, moving it from the Landing Zone all the way to the Curated Zone.

1.  **Customer Sanity Check (`Customer_curated_job`)**
    * **Goal:** Create a clean list of customers.
    * **Action:** Filters the raw customer data to only include customers who have both **agreed to share data** *AND* have associated **Accelerometer data**. The result is stored in the `customers_curated` table.

2.  **Step Trainer Filtering (`Steptrainer_trusted_job`)**
    * **Goal:** Clean the Step Trainer data.
    * **Action:** Uses the clean list from Step 1 (`customers_curated`) to filter the raw Step Trainer data. This ensures the `step_trainer_trusted` table only contains records for known, consenting users.

3.  **ML Data Aggregation (`Machinelearning_curated_job`)**
    * **Goal:** Create the final, usable ML dataset.
    * **Action:** **Joins** the clean Step Trainer data with the corresponding Accelerometer data using the `timestamp` as the key. This final, joined dataset is saved as the **`machine_learning_curated`** table.

---

## 💻 Setup & Running the Project

### Prerequisites

You need a working AWS environment with permissions for:
* **AWS S3** (for data storage)
* **AWS Glue** (for ETL jobs and the Data Catalog)
* **Amazon Athena** (for testing and querying)

### Steps to Replicate

1.  **S3 Buckets:** Set up your S3 buckets. The current configuration uses the bucket path `s3://finalprojectsaleem/`. Make sure your data files (Customer, Accelerometer, Step Trainer) are uploaded to the respective **`/landing/`** paths.
2.  **Database & Tables:** Use the provided SQL scripts (e.g., `customer_landing.sql`) in **Amazon Athena** or set up **Glue Crawlers** to create the initial tables in the `finaldatabase` schema.
3.  **Upload Glue Scripts:** Upload the Python (`.py`) scripts for the three Glue jobs to your designated S3 script location.
4.  **Run Jobs:** Execute the three AWS Glue jobs in the correct order (1, 2, then 3) to process the data and populate the Trusted and Curated zones.

### Final Output

After the jobs run, you can query the final, clean dataset in Athena:

```sql
-- Query the final dataset for the ML team
SELECT *
FROM finaldatabase.machine_learning_curated
LIMIT 50;
