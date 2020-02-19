import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import datasets
from sklearn.metrics import mean_squared_error
import seaborn as sns

from sklearn import linear_model

#  Load the data set. Use the pandas module to read the data from the file system. Check few records of the dataset.
names = ['memory','url','cpu'] #, 'nio', 'work', 'nav'
data = pd.read_csv('final',names=names)
print(data.head())

# Checking the statistical values of the dataset using the describe() function.
print(data.describe())

# check for null values if any present in the dataset.
print(data.isnull().sum())

# EDA : Exploratory Data Analysis is a very important step before training the model.
# We will use some visualizations to understand the relationship of the target variable with other variables.
sns.distplot(data) 