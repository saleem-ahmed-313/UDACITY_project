# 📊 IoT Data Lake & ML Curation Pipeline

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![AWS](https://img.shields.io/badge/Tech-AWS_Glue-orange?style=flat&logo=amazon-aws)](https://aws.amazon.com/glue/)
[![Data-Lake](https://img.shields.io/badge/Zone-Curated_Data-informational)](https://en.wikipedia.org/wiki/Data_lake)

---

## 🌟 Project Overview

This project implements a **serverless Data Lake ETL (Extract, Transform, Load) pipeline** on AWS. It is designed to process and curate data from various Internet of Things (IoT) devices and customer records, specifically focusing on **Customer, Accelerometer, and Step Trainer** data.

The primary goal is to **sanitize, transform, and aggregate** the data through distinct Data Lake zones (**Landing, Trusted, and Curated**) to produce a high-quality, joined dataset optimized for downstream machine learning (ML) consumption.

---

## 🔑 Key Features

* **Data Ingestion & Schema Definition**: Defines initial Glue Tables (`customer_landing`, `accelerometer_landing`, `step_trainer_landing`) using provided SQL scripts.
* **Customer Sanitization**: A Glue job filters and promotes only customers who have **agreed to share their data** and possess associated accelerometer records to the **Curated Zone** (`customers_curated`).
* **Trusted Zone Filtering**: Creates a **Trusted Zone** table (`step_trainer_trusted`) containing Step Trainer records specifically for the vetted customers.
* **ML Data Aggregation**: The final Glue job joins the `Step Trainer` data with corresponding `Accelerometer` data based on timestamp, creating the final **Machine Learning Curated** table (`machine_learning_curated`).
* **Serverless & Scalable**: Leverages AWS Glue and S3 for a fully managed, scalable, and cost-efficient architecture.

---

## 🏗️ Architecture & Data Flow

The pipeline processes data sequentially across three key Data Lake zones:

| Zone | Primary Table(s) | Purpose |
| :--- | :--- | :--- |
| **Landing** | `customer_landing`, `accelerometer_landing`, `step_trainer_landing` | Raw, un-modified source data. |
| **Trusted** | `step_trainer_trusted` | Cleansed, standardized, and partitioned data. |
| **Curated** | `customers_curated`, `machine_learning_curated` | Aggregated, business-ready data for ML. |

### ETL Job Summary

| Job Name | Source(s) | Target Table |
| :--- | :--- | :--- |
| **Customer Curated** | `customer_trusted`, `accelerometer_landing` | `customers_curated` |
| **Step Trainer Trusted** | `step_trainer_landing`, `customers_curated` | `step_trainer_trusted` |
| **ML Aggregation** | `step_trainer_trusted`, `accelerometer_trusted` | `machine_learning_curated` |

---

## 🚀 Getting Started

To replicate and run this project, follow these general steps:

### Prerequisites
* An active **AWS Account**.
* **AWS CLI** configured.
* Access and permissions for **AWS Glue** (ETL), **Amazon S3** (Storage), and **Amazon Athena** (Querying).

### Installation & Deployment

1.  **Clone the Repository**
    ```bash
    git clone [YOUR_REPO_URL]
    cd [YOUR_PROJECT_FOLDER]
    ```
2.  **S3 Setup**: Ensure your S3 buckets are set up according to your Glue table locations (e.g., `s3://finalprojectsaleem/customer/landing/`).
3.  **Upload Scripts**: Upload all `*.sql` and Glue job Python scripts to the designated S3 script path.
4.  **Define Tables**: Run the initial DDL scripts (`customer_landing.sql`, etc.) via **Athena** or configure **Glue Crawlers** to create the initial tables in the `finaldatabase`.
5.  **Execute Glue Jobs**: Trigger the three main Glue jobs in the correct order to populate the Trusted and Curated zones.

---

## 🛠️ Usage

Once the pipeline completes, the final aggregated data is ready for analysis and machine learning:

1.  **Query Data**: Use **Amazon Athena** to query the final dataset:

    ```sql
    -- Example: View a sample of the prepared ML data
    SELECT *
    FROM finaldatabase.machine_learning_curated
    LIMIT 100;
    ```
2.  **Machine Learning**: The `machine_learning_curated` table can be directly linked to **Amazon SageMaker** notebooks for model training and feature engineering.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## 📧 Contact

For any questions or suggestions, please open an issue on the GitHub repository.
