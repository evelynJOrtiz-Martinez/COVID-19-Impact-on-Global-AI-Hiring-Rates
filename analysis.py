import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import os

def clean_percentage(value):
    """Convert percentage string to float"""
    try:
        if isinstance(value, str) and '%' in value:
            return float(value.replace('%', ''))
        return float(value)
    except:
        return np.nan

def analyze_covid_impact(file_path):
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} was not found")
            
        # Read the data
        print(f"Reading data from {file_path}...")
        df = pd.read_csv(file_path)
        
        # Convert percentage strings to floats for all columns except Date
        print("Converting percentage values...")
        for column in df.columns:
            if column != 'Date':
                df[column] = df[column].apply(clean_percentage)
        
        # Data Preprocessing
        print("\nPreprocessing data...")
        # 1. Convert date column to datetime
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')
        
        # 2. Add year column for easier analysis
        df['Year'] = df['Date'].dt.year
        
        # 3. Calculate statistics for different periods
        print("Calculating statistics for different periods...")
        # Pre-COVID (2018-2019)
        pre_covid = df[df['Year'].isin([2018, 2019])]
        # During COVID (2020-2022)
        during_covid = df[df['Year'].isin([2020, 2021, 2022])]
        # Post-COVID (2023)
        post_covid = df[df['Year'] == 2023]
        
        # Calculate metrics
        results = {}
        
        # 1. Calculate mean hiring rates for each period by country
        countries = [col for col in df.columns if col not in ['Date', 'Year']]
        
        print("Analyzing country-specific impacts...")
        for country in countries:
            pre_mean = pre_covid[country].mean()
            during_mean = during_covid[country].mean()
            post_mean = post_covid[country].mean()
            
            # Calculate percentage change from pre to during COVID
            pct_change = ((during_mean - pre_mean) / pre_mean) * 100
            
            results[country] = {
                'pre_covid_mean': pre_mean,
                'during_covid_mean': during_mean,
                'post_covid_mean': post_mean,
                'pct_change_during_covid': pct_change
            }
        
        # Convert results to DataFrame for easier analysis
        results_df = pd.DataFrame(results).T
        
        # Calculate global metrics
        print("Calculating global metrics...")
        global_metrics = {
            'mean_pct_change': results_df['pct_change_during_covid'].mean(),
            'median_pct_change': results_df['pct_change_during_covid'].median(),
            'std_pct_change': results_df['pct_change_during_covid'].std(),
            'most_impacted_country': results_df['pct_change_during_covid'].idxmin(),
            'most_impacted_value': results_df['pct_change_during_covid'].min(),
            'least_impacted_country': results_df['pct_change_during_covid'].idxmax(),
            'least_impacted_value': results_df['pct_change_during_covid'].max()
        }
        
        # Perform t-test between pre-COVID and during-COVID periods
        t_stat, p_value = stats.ttest_ind(
            df[df['Year'].isin([2018, 2019])].iloc[:, 1:-1].values.flatten(),
            df[df['Year'].isin([2020, 2021, 2022])].iloc[:, 1:-1].values.flatten()
        )
        
        global_metrics['t_statistic'] = t_stat
        global_metrics['p_value'] = p_value
        
        return results_df, global_metrics
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None, None

def create_visualizations(results_df, global_metrics):
    """Create and save visualizations of the analysis results"""
    # Set style parameters directly
    plt.style.use('default')  # Use default style instead of seaborn
    # Set custom colors for consistency
    colors = ['#4A148C', '#9C27B0', '#1A237E', '#3F51B5']
    
    # 1. Impact by Country (Horizontal Bar Chart)
    plt.figure(figsize=(12, 8))
    results_sorted = results_df.sort_values('pct_change_during_covid')
    bars = plt.barh(results_sorted.index, results_sorted['pct_change_during_covid'])
    plt.title('COVID-19 Impact on AI Hiring Rates by Country', fontsize=12, pad=20)
    plt.xlabel('Percentage Change During COVID (%)')
    plt.ylabel('Country')
    # Color bars based on value
    for bar in bars:
        bar.set_color(colors[0] if bar.get_width() < 0 else colors[2])
    plt.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('impact_by_country.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Box Plot of Pre vs During COVID Rates
    plt.figure(figsize=(10, 6))
    box_data = {
        'Pre-COVID': results_df['pre_covid_mean'],
        'During COVID': results_df['during_covid_mean'],
        'Post-COVID': results_df['post_covid_mean']
    }
    plt.boxplot(box_data.values(), labels=box_data.keys(), patch_artist=True)
    plt.title('Distribution of AI Hiring Rates Across Different Periods', fontsize=12, pad=20)
    plt.ylabel('Relative AI Hiring Rate')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('period_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 3. Top 10 Most Impacted Countries
    plt.figure(figsize=(12, 6))
    worst_10 = results_sorted['pct_change_during_covid'].head(10)
    plt.bar(worst_10.index, worst_10, color=colors[0])
    plt.title('10 Most Impacted Countries', fontsize=12, pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Percentage Change During COVID (%)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('top_10_impacted.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 4. Recovery Analysis
    plt.figure(figsize=(12, 6))
    recovery_data = pd.DataFrame({
        'During COVID Impact': results_df['pct_change_during_covid'],
        'Post/Pre COVID Ratio': ((results_df['post_covid_mean'] - results_df['pre_covid_mean']) / 
                                results_df['pre_covid_mean'] * 100)
    })
    plt.scatter(recovery_data['During COVID Impact'], 
                recovery_data['Post/Pre COVID Ratio'],
                color=colors[1],
                alpha=0.6)
    plt.xlabel('Impact During COVID (%)')
    plt.ylabel('Post vs Pre-COVID Change (%)')
    plt.title('COVID Impact vs Recovery Analysis', fontsize=12, pad=20)
    # Add quadrant lines
    plt.axhline(y=0, color='gray', linestyle='--', alpha=0.3)
    plt.axvline(x=0, color='gray', linestyle='--', alpha=0.3)
    plt.grid(True, alpha=0.3)
    
    # Add labels for notable points
    for idx, row in recovery_data.iterrows():
        if abs(row['During COVID Impact']) > 50 or abs(row['Post/Pre COVID Ratio']) > 50:
            plt.annotate(idx, 
                        (row['During COVID Impact'], row['Post/Pre COVID Ratio']),
                        xytext=(5, 5), 
                        textcoords='offset points',
                        fontsize=8)
    
    plt.tight_layout()
    plt.savefig('recovery_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("\nVisualizations have been saved as PNG files in your working directory:")
    print("1. impact_by_country.png - Shows the impact for all countries")
    print("2. period_distribution.png - Shows the distribution of rates across different periods")
    print("3. top_10_impacted.png - Highlights the 10 most impacted countries")
    print("4. recovery_analysis.png - Shows the relationship between impact and recovery")
    

def print_results(results_df, global_metrics):
    if results_df is None or global_metrics is None:
        return
    
    print("\n=== Global Impact Summary ===")
    print(f"Mean percentage change during COVID: {global_metrics['mean_pct_change']:.2f}%")
    print(f"Median percentage change during COVID: {global_metrics['median_pct_change']:.2f}%")
    print(f"Standard deviation of change: {global_metrics['std_pct_change']:.2f}%")
    
    print(f"\n=== Most and Least Impacted Countries ===")
    print(f"Most impacted country: {global_metrics['most_impacted_country']} ({global_metrics['most_impacted_value']:.2f}%)")
    print(f"Least impacted country: {global_metrics['least_impacted_country']} ({global_metrics['least_impacted_value']:.2f}%)")
    
    print(f"\n=== Statistical Significance ===")
    print(f"t-statistic: {global_metrics['t_statistic']:.2f}")
    print(f"p-value: {global_metrics['p_value']:.4f}")
    
    print("\n=== Top 5 Most Negatively Impacted Countries ===")
    print(results_df.sort_values('pct_change_during_covid').head()['pct_change_during_covid'])
    
    print("\n=== Top 5 Least Impacted/Positive Growth Countries ===")
    print(results_df.sort_values('pct_change_during_covid', ascending=False).head()['pct_change_during_covid'])

if __name__ == "__main__":
    # Specify the path to your CSV file
    file_path = "fig_4.2.13.csv"  # Make sure this matches your file name and location
    
    # Run the analysis
    print("Starting analysis...")
    results_df, global_metrics = analyze_covid_impact(file_path)

    print("\nGenerating visualizations...")
    create_visualizations(results_df, global_metrics)
    
    # Print results
    print_results(results_df, global_metrics)
