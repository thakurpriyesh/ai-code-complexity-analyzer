import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import streamlit as st

@st.cache_resource
def train_model():
    """Generates synthetic dataset and trains a scikit-learn Pipeline."""
    np.random.seed(42)
    n_samples = 5000
    
    # Generate realistic distributions for code features
    loops = np.random.poisson(2, n_samples)
    conditionals = np.random.poisson(3, n_samples)
    functions = np.random.poisson(1.5, n_samples)
    variables = np.random.poisson(5, n_samples)
    classes = np.random.poisson(0.5, n_samples)
    max_depth = np.ceil((loops + conditionals) / 3).astype(int) + np.random.randint(0, 2, n_samples)
    
    # Calculate a "true" complexity score to act as the label
    complexity_label = (loops * 2) + conditionals + (max_depth * 1.5) + (variables * 0.1) + np.random.normal(0, 1, n_samples)
    complexity_label = np.maximum(1, np.round(complexity_label))
    
    df = pd.DataFrame({
        'loops': loops, 'conditionals': conditionals, 'functions': functions, 
        'variables': variables, 'classes': classes, 'max_depth': max_depth, 
        'complexity_label': complexity_label
    })
    
    X = df[['loops', 'conditionals', 'functions', 'variables', 'classes', 'max_depth']]
    y = df['complexity_label']
    
    # Define the Industry-Standard ML Pipeline
    pipeline = Pipeline([
        ('scaler', StandardScaler()),  # Step 1: Standardize features by removing the mean and scaling to unit variance
        ('regressor', RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42))  # Step 2: Train the model
    ])
    
    # Fit the entire pipeline
    pipeline.fit(X, y)
    
    return pipeline