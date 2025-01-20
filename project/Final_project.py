import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from matplotlib.colors import LinearSegmentedColormap
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr
import seaborn as sns
import warnings
import os

warnings.filterwarnings("ignore", category=FutureWarning)

# Function to load data from SQLite
def load_data_from_sqlite():
    db_path = r'C:\Users\zaian\OneDrive\Desktop\Zaian-made-template\data\merged_mental_marriage_data.sqlite'
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM mental_Marriage_Data;"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Standardize state names
    df['State'] = df['State'].str.strip().str.title()

    # Calculate average marriage rate
    df['Average Marriage Rate'] = df[['Marriage rates per 1,000 in 2021', 'Marriage rates per 1,000 in 2022']].mean(axis=1)
    return df

# Function to create heatmap
def create_correlation_heatmap(df):
    # Select all numeric columns for the heatmap
    heatmap_data = df.select_dtypes(include=['float64', 'int64']).corr()

    # Plot the heatmap
    plt.figure(figsize=(14, 10))
    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt=".2f",
        cmap='coolwarm',
        center=0,
        linewidths=0.5
    )
    plt.title('Correlation Heatmap (All Factors)', fontsize=16)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()

    # Save the heatmap as an image
    if not os.path.exists('maps'):
        os.makedirs('maps')
    plt.savefig('maps/correlation_heatmap_all_factors.png', dpi=300)
    plt.close()
    
# Function to create choropleth maps
def create_choropleth_maps(df):
    # Load and prepare state geometries
    states = gpd.read_file('https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_state_20m.zip')

    # Standardize state names
    states['name'] = states['NAME'].str.title()
    df['State'] = df['State'].str.title()

    # Filter continental states but keep Alaska and Hawaii
    continental = states[~states['NAME'].isin(['Puerto Rico'])]

    # Define color maps
    orange_white_colors = ['#FFEDA0', '#FEB24C', '#F03B20']
    orange_cmap = LinearSegmentedColormap.from_list('custom_orange', orange_white_colors)
    blue_colors = ['#EFF3FF', '#C6DBEF', '#9ECAE1', '#6BAED6', '#4292C6', '#2171B5', '#084594']
    blue_cmap = LinearSegmentedColormap.from_list('custom_blues', blue_colors)

    # Columns to map
    columns_to_map = {
        'Average Marriage Rate': orange_cmap,
        'Any Mental Illness 26+ (%)': blue_cmap,
        'Serious Mental Illness 26+ (%)': blue_cmap,
        'Received Mental Health Treatment 26+ (%)': blue_cmap,
        'Major Depressive Episode 26+ (%)': blue_cmap,
        'Thoughts of Suicide 26+ (%)': blue_cmap,
        'Made Any Suicide Plans 26+ (%)': blue_cmap,
        'Attempted Suicide 26+ (%)': blue_cmap
    }

    for column, cmap in columns_to_map.items():
        fig, ax = plt.subplots(figsize=(15, 10))
        merged = continental.merge(df, left_on='name', right_on='State', how='left')
        merged[column] = pd.to_numeric(merged[column], errors='coerce')
        
        try:
            merged.plot(
                column=column,
                ax=ax,
                legend=True,
                legend_kwds={'label': column},
                missing_kwds={'color': 'lightgrey'},
                cmap=cmap
            )
            
            # Add state labels
            for idx, row in merged.iterrows():
                if row.geometry is not None:
                    centroid = row.geometry.centroid
                    ax.annotate(
                        text=row['STUSPS'],
                        xy=(centroid.x, centroid.y),
                        horizontalalignment='center',
                        verticalalignment='center',
                        fontsize=8
                    )
            
            ax.set_xlim([-125, -65])
            ax.set_ylim([25, 50])
            ax.axis('off')
            plt.title(f'{column} by State')
            
            # Save map
            if not os.path.exists('maps'):
                os.makedirs('maps')
            plt.savefig(f'maps/{column.replace("/", "_").replace(" ", "_")}_map.png', 
                        bbox_inches='tight', dpi=300)
        except Exception as e:
            print(f"Error creating map for {column}: {e}")
        finally:
            plt.close()

# Function to calculate correlations
def correlation_analysis_with_states(df):
    marriage_rate_col = 'Average Marriage Rate'
    correlations = []

    # Only include 26+ (%) metrics for mental health
    mental_health_columns = [
        'Any Mental Illness 26+ (%)',
        'Serious Mental Illness 26+ (%)',
        'Received Mental Health Treatment 26+ (%)',
        'Major Depressive Episode 26+ (%)',
        'Thoughts of Suicide 26+ (%)',
        'Made Any Suicide Plans 26+ (%)',
        'Attempted Suicide 26+ (%)'
    ]

    for health_col in mental_health_columns:
        try:
            overall_corr, p_value = pearsonr(df[marriage_rate_col], df[health_col])
        except Exception as e:
            print(f"Error calculating correlation for {health_col}: {e}")
            overall_corr, p_value = None, None

        # Add state-level correlations
        for state in df['State'].unique():
            state_data = df[df['State'] == state]
            if not state_data.empty:
                try:
                    marriage_rate = state_data[marriage_rate_col].iloc[0]
                    health_rate = state_data[health_col].iloc[0]
                    correlations.append({
                        'State': state,
                        'Marriage Rate': round(marriage_rate, 3),
                        'Mental Health Metric': health_col,
                        'Mental Health Value': round(health_rate, 3),
                        'Overall Correlation': round(overall_corr, 3) if overall_corr is not None else '',
                        'P-value': round(p_value, 3) if p_value is not None else ''
                    })
                except Exception as e:
                    print(f"Error processing state {state} for metric {health_col}: {e}")
                    continue

    # Convert to DataFrame
    corr_df = pd.DataFrame(correlations)

    # Extract top 3 correlations
    top_3 = corr_df.drop_duplicates('Mental Health Metric').nlargest(3, 'Overall Correlation')
    return corr_df, top_3

# Function to print top correlations
def print_top_correlations(top_3):
    print("\nTop 3 Strongest Correlations:")
    print("=" * 80)
    for _, row in top_3.iterrows():
        print(f"Mental Health Metric: {row['Mental Health Metric']}")
        print(f"Correlation: {row['Overall Correlation']:.3f}")
        print(f"P-value: {row['P-value']:.3f}")
        print("-" * 80)

def perform_regression_analysis(df):
    """
    Perform linear regression for Average Marriage Rate as the dependent variable
    and each mental health metric as an independent variable.
    """
    results = []
    top_metrics = [
        "Serious Mental Illness 26+ (%)",
        "Thoughts of Suicide 26+ (%)",
        "Major Depressive Episode 26+ (%)"
    ]
    X = df[top_metrics]
    y = df['Average Marriage Rate']

    for metric in top_metrics:
        X_single = df[[metric]].dropna()
        y_single = y[X_single.index]
        if len(X_single) > 1:  # Ensure sufficient data for regression
            model = LinearRegression()
            model.fit(X_single, y_single)

            # Calculate regression statistics
            coef = model.coef_[0]
            intercept = model.intercept_
            r_squared = model.score(X_single, y_single)
            p_value = pearsonr(X_single[metric], y_single)[1]  # Calculate p-value

            results.append({
                "Metric": metric,
                "Coefficient": coef,
                "Intercept": intercept,
                "R-squared": r_squared,
                "P-value": p_value
            })

    # Combine metrics for multiple regression
    X_combined = X.dropna()
    y_combined = y[X_combined.index]
    if len(X_combined) > 1:
        model = LinearRegression()
        model.fit(X_combined, y_combined)

        combined_r_squared = model.score(X_combined, y_combined)

        print("\nMultiple Regression:")
        print(f"R-squared: {combined_r_squared:.3f}")

    # Save regression results
    results_df = pd.DataFrame(results)
    results_df.to_csv('maps/regression_analysis.csv', index=False)

    print("\nRegression Analysis Results:")
    print(results_df)

    return results_df

def create_scatterplots_with_regression(df):
    """
    Create scatterplots with regression lines for Average Marriage Rate vs top mental health metrics.
    """
    top_metrics = [
        "Serious Mental Illness 26+ (%)",
        "Thoughts of Suicide 26+ (%)",
        "Major Depressive Episode 26+ (%)"
    ]
    for metric in top_metrics:
        plt.figure(figsize=(10, 6))
        X = df[[metric]].dropna()
        y = df['Average Marriage Rate'][X.index]

        if len(X) > 1:
            # Fit linear regression
            model = LinearRegression()
            model.fit(X, y)

            # Scatterplot
            plt.scatter(X, y, label='Data Points', alpha=0.8)
            plt.plot(X, model.predict(X), color='red', label='Regression Line')

            # Annotate correlation and p-value
            correlation, p_value = pearsonr(X[metric], y)
            plt.annotate(
                f"r = {correlation:.3f}\nP-value = {p_value:.3f}",
                xy=(0.05, 0.85),
                xycoords='axes fraction',
                fontsize=12,
                bbox=dict(boxstyle="round", fc="white", ec="black", alpha=0.8)
            )

            # Formatting
            plt.title(f"Scatterplot: Average Marriage Rate vs {metric}")
            plt.xlabel(metric)
            plt.ylabel("Average Marriage Rate")
            plt.legend()
            plt.grid(alpha=0.3)

            # Save the plot
            metric_clean = metric.replace(" ", "_").replace("%", "").replace("+", "Plus")
            plt.savefig(f'maps/scatterplot_{metric_clean}.png', bbox_inches='tight', dpi=300)

        plt.close()
        
# Main function
def main():
    # Load data
    df = load_data_from_sqlite()

    # Create visualizations
    create_choropleth_maps(df)
    
    # Create correlation heatmap with selected columns
    create_correlation_heatmap(df)
    
    # Perform regression analysis
    regression_results = perform_regression_analysis(df)

    # Create scatterplots with regression lines
    create_scatterplots_with_regression(df)

    # Perform correlation analysis
    corr_df, top_3 = correlation_analysis_with_states(df)

    # Save correlation results and print top correlations
    corr_df.to_csv('maps/correlation_results.csv', index=False)
    print_top_correlations(top_3)



if __name__ == "__main__":
    main()

