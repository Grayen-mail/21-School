Heart Disease UCI
==============================

## Data

Download [data](https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset/download?datasetVersionNumber=2) and 
extract into folder `../datasets/heart.csv`

## Setup Virtual Environment
~~~
cd src
python -m venv heart_venv
source heart_venv/bin/activate
pip install -r requirements.txt
~~~

## Train
#### Logistic Regression
~~~
python heart/train.py hydra.job.chdir=True model=lr
~~~
#### Random forest
~~~ 
python heart/train.py hydra.job.chdir=True model=rf
~~~

## Test:
~~~
pytest tests
~~~

## Linter:
~~~
pylint heart
~~~

## Project Organization
    ├── datasets                <- Datasets for use in this project.
    ├── src                     <- Source code for use in this project.
    │   ├── configs             <- Configuration files
    │   ├── heart               <- Source code
    │   │   ├── data            <- Loads and preparing dataset
    │   │   ├── entities        <- Configuration ORM entities
    │   │   ├── futures         <- Futures prepare and process
    │   │   ├── models          <- Code to train models and then use trained models to make
    │   │   ├── __init__.py     <- Makes heart a Python module
    │   │   └── train.py        <- Script for training model
    │   ├── heart_venv          <- Python virtual environment
    │   ├── tests               <- Tests files for this project
    │   │
    │   ├── artefacts           <- Hydra artefacts
    │   │   └── ${now:%Y-%m-%d_%H-%M-%S}  <- Artefacts for every command
    │   │       ├── train.log   <- Train logs
    │   │       ├── models      <- Trained and serialized models, model predictions, or model summaries
    │   │       └── metrics               <- Models metrics
    │   ├── tests               <- unit & integration tests
    │   ├── LICENSE
    │   ├── README.md          <- The top-level README for developers using this project.
    │   └── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
                                  generated with `pip freeze > requirements.txt`
