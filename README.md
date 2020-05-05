![Udacity Logo](./data/udacity_logo.png)

# Recommendation at the Starbucks Rewards App

This repository contains an implementation of a recommender system for Starbucks rewards app, a project submitted to Udacity's Machine Learning Engineer nanodegree. 

The `project_report.pdf` contains a thorough submitted report, explaining the problem to be solved, analysis of the datasets, proposed methodologies and results. 

## Overview

Reward systems have been widely used to enhance customers’ engagement
in digital-based platforms. By offering these users a challenge and a correspondent
reward, they not only can be attracted to have more interactions with
a company’s service, but most importantly it can lead them into becoming frequent
users, thus enhancing a brand’s impact on its customers. However, knowing
which challenge to provide can be a rather complex task since each customer
profile responds differently to each offer. In order to overcome this problem, this
project proposes a multi-armed bandit recommendation system that uses historical rewards usage
to build a data-driven users’ profiles so as to model the most suitable offer type
to each profile.


## Dependencies

As part of the Machine Learning Nanodegree, the current project was developed under Amazon's Sagemaker enviroment. In this sense, some of the functions require that the notebooks are executed with access to an S3 bucket.

In order to install the dependent libraries, run the following command:

```bash
pip install squarify powerlaw joblib boto3 pickle sklearn
```

## Repository Structure

The repository tree is organized as follows: 

```
├───data
├───notebooks
│   └───plots
├───scripts
└───sources
    ├───funk_svd
    ├───mab    
```

The `data` folder contains the necessary dataset to execute the whole project and it is used to store any relevant variables. The `notebooks` folder contains jupyter notebooks used for exploratory data analysis and model training, as well as their generated plots. The `scripts` repository contains files relevant to custom libraries developed throughout the project. These libraries are stored in the `sources` folder. 

## Execution 

In order to obtain the results of this project, run the following notebooks (in this order)

- `notebooks/exploratory_data_analysis.ipynb`
- `notebooks/model_training_validation.ipynb`


