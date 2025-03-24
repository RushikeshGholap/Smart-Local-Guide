# Smart Local Guide – Capstone Project

Welcome to our **Smart Local Guide** repository. This project aims to develop a robust recommender system that leverages **Google Reviews**, accompanying metadata, and advanced **Natural Language Processing** (NLP) techniques to provide users with highly relevant local business recommendations.

---

## Table of Contents
1. [Team Overview](#team-overview)  
2. [Project Overview](#project-overview)  
3. [Key Features](#key-features)  
4. [Data Pipeline](#data-pipeline)  
5. [Database & Filtering](#database--filtering)  
6. [Future Enhancements](#future-enhancements)  
7. [Capstone Presentation](#capstone-presentation)  
8. [Capstone Report](#capstone-report)  
9. [Capstone Playground Notebooks Merged](#capstone-playground-notebooks-merged)  
10. [Contributing](#contributing)  
11. [License](#license)

---

## Team Overview
**Group 9: The Eagles** brings together a diverse range of expertise to develop the **Smart Local Guide** recommender system. Each member contributed to various aspects of the project, ensuring a well-rounded approach and a thorough execution of tasks.

### Team Members & Roles
- **Rushikesh Gholap**  
  *Data discovery, Data Flow, Architecture & Exploratory Data Analysis (EDA)*  

- **Jelitta James**  
  *Data Cleaning, Pre-processing & EDA, Noise analysis*  

- **Hassaan Alvi**  
  *Data Cleaning, Reports, Pre-processing & EDA*  

- **Priyanka Choudhary**  
  *Pre-processing, Documentation, EDA & Feature Engineering*  

- **Krish Balar**  
  *Data Cleaning, Pre-processing, EDA & Feature Engineering*  

### Collaboration
Our team collaborated regularly via:
- **Virtual Meetings**: Consistent Zoom calls to discuss progress, roadblocks, and future milestones.  
- **Daily Messaging**: Rapid communication through instant messaging platforms to address day-to-day queries and updates.  
- **Shared Tools**: Google Drive for documentation and file sharing, GitHub for version control and code collaboration.

---

## Project Overview
**Smart Local Guide** is designed to offer personalized recommendations by analyzing:
- **Large-scale review data** (ratings, text, timestamps) from Google Local Reviews.  
- **Business metadata** (category, location, average ratings, etc.).  
- **User engagement metrics** (review frequency, sentiment analysis).  

Our goal is to seamlessly recommend businesses (initially focusing on Pennsylvania) while addressing real-world data challenges such as data cleaning, outlier management, and noise detection.
---

## Project Overview
**Smart Local Guide** is designed to offer personalized recommendations by analyzing:
- **Large-scale review data** (ratings, text, timestamps) from Google Local Reviews.  
- **Business metadata** (category, location, average ratings, etc.).  
- **User engagement metrics** (review frequency, sentiment analysis).  

Our goal is to seamlessly recommend businesses (initially focusing on Pennsylvania) while dealing with real-world data challenges such as data cleaning, outlier management, and noise detection.

---

## Key Features
- **Sentiment Analysis**: Harnessing NLP techniques to derive sentiment signals that complement star ratings.  
- **Feature Engineering**: Converting unstructured text into features suitable for modeling (e.g., One-Hot Encoding, Truncated SVD).  
- **Noise & Outlier Detection**: Identifying fake/dormant users and skewed rating patterns to refine recommendations.  
- **Large-Scale Handling**: Using optimized database queries and batch processing to handle extensive datasets.  

---

## Data Pipeline
1. **Data Ingestion**: We source our dataset from the [Google Local Reviews dataset](https://cseweb.ucsd.edu/~jmcauley/datasets.html) (UCSD McAuley Group).  
2. **Preprocessing**:  
   - Remove duplicates and highly sparse features.  
   - Convert timestamps to human-readable dates.  
   - Impute missing values and standardize text.  
3. **Exploratory Data Analysis (EDA)**:  
   - Identify data distribution, outliers, and missing patterns.  
   - Analyze rating trends, review frequencies, and user behavior.  
4. **Feature Engineering**:  
   - Extract meaningful categorical features from unstructured data.  
   - Dimensionality reduction (Truncated SVD) for high-dimensional vectors.  

---

## Database & Filtering
All project-related data is persisted in a **PostgreSQL** database. During model training and system usage, **only the relevant filtered records** are queried to:
- **Improve performance** by loading smaller, targeted subsets.  
- **Exclude noise** or out-of-scope businesses based on well-defined criteria.  

All **filtering criteria** (e.g., removing low-rated and inactive businesses, ignoring spam-like reviews) are discussed thoroughly in our presentation. These criteria can be **easily updated** as the system evolves.

---


## Future Enhancements
- **Extend Categories**: Currently focusing on the food industry, but can easily include more categories (e.g., retail, hospitality).  
- **Refine Filtering Criteria**: Additional business attributes or advanced heuristics to remove noisy data.  
- **Real-Time Recommendations**: Integrate streaming pipelines (e.g., Spark Streaming) for up-to-date suggestions.  
- **Scalability**: Deploy on a cloud platform with containerization (Docker/Kubernetes) for horizontal scaling.

---

## Capstone Presentation
To view a comprehensive walkthrough of our project’s methodology, data filtering criteria, and next steps, please see our **[Capstone Presentation](https://docs.google.com/presentation/d/13t4itNW0MNPbDdH4nBo2e_Wpl3p4tFpvn1CFQEFywoQ/)**. This document covers detailed insights into the decisions and strategies adopted throughout development.

---


## Capstone Report
To view a well documented rerpot and  walkthrough of our project’s methodology, data filtering criteria, please see our **[Capstone Report](https://github.com/RushikeshGholap/Capstone-Google-Maps-Recommender/blob/main/Presentation%26Reports/Exploratory%20Data%20Analysis%20Report%20G9-The%20Eagles.pdf)**. This document covers detailed EDA into the decisions and strategies adopted throughout development.

---


## Capstone Playground Notebooks Merged
This is our merged EDA notebook were you can find code snippets, data filtering criteria, please see our **[Capstone EDA Merged](https://github.com/RushikeshGholap/Capstone-Google-Maps-Recommender/blob/main/Main_Cleaning_dumping_%26_EDA_merged.ipynb))**. This notebook is merged version of all members working on there respective playground notebook, thus may not be in best descriptive state, but we will try to update it along with Capstone II. Usage of this notebook is how we work with data and perform EDA and Analysis. 

---

## Contributing
We are working as team on Capstone. Only our team members can make changes or commit to this repo. Its managed by out Capstone Team.

---

## License
This project is licensed under the [MIT License](LICENSE). Feel free to use, distribute, or modify this code under the terms of the license.

---

**Thank you** for visiting our repository! We look forward to collaborating with you to make **Smart Local Guide** a powerful and user-friendly local recommender system. If you have any questions, please open an issue or contact one of our team members.
