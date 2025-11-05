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
## 🛠️ Technology Stack

* **Cloud Platform:** Amazon Web Services (AWS)
* **ETL/Data Processing:** AWS Glue
* **Storage:** Amazon S3
* **Querying:** Amazon Athena
* **Language:** SQL and Python (within Glue)

