"""
Visualization utilities for exploratory data analysis.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Optional, Union

def setup_plot_style() -> None:
    """Set up consistent plotting style."""
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = [12, 8]
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.labelsize'] = 14
    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12

def plot_distributions(
    data: pd.DataFrame, 
    columns: Optional[List[str]] = None, 
    figsize: tuple = (15, 10)
) -> None:
    """
    Plot distributions of numerical columns.
    
    Args:
        data: Input DataFrame
        columns: List of columns to plot. If None, plot all numerical columns.
        figsize: Figure size (width, height)
    """
    if columns is None:
        columns = data.select_dtypes(include=['number']).columns.tolist()
    
    n_cols = 2
    n_rows = (len(columns) + 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = axes.flatten()
    
    for i, col in enumerate(columns):
        if i < len(axes):
            sns.histplot(data[col], kde=True, ax=axes[i])
            axes[i].set_title(f'Distribution of {col}')
    
    # Hide any remaining empty subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])
    
    plt.tight_layout()
    plt.show()

def plot_correlation_heatmap(
    data: pd.DataFrame, 
    method: str = 'pearson',
    figsize: tuple = (12, 10),
    **kwargs
) -> None:
    """
    Plot a correlation heatmap for numerical columns.
    
    Args:
        data: Input DataFrame
        method: Correlation method ('pearson', 'spearman', 'kendall')
        figsize: Figure size (width, height)
        **kwargs: Additional arguments to pass to sns.heatmap()
    """
    plt.figure(figsize=figsize)
    corr = data.select_dtypes(include=['number']).corr(method=method)
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    sns.heatmap(
        corr, 
        mask=mask,
        annot=True, 
        fmt='.2f',
        cmap='coolwarm',
        vmin=-1, 
        vmax=1,
        **kwargs
    )
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.show()
