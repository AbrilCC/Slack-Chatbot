import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def analyze_jobs_csv(file_path, category):
    df = pd.read_csv(file_path)
    df = df.dropna(subset=['Data_value'])
    data_col = 'Series_title_2'

    #Select only specific rows
    if category == "industry":
        df = df[df['Group'] == "Industry by employment variable"]
    elif category == "sex":
        df = df[df['Group'] == "Sex by employment variable"]
    elif category == "age":
        df = df[df['Group'] == "Age by employment variable"]
    
    #Discard null data
    df = df[df['Series_title_2'].notna()]
    df = df[df['Series_title_3'].isin(["Seasonally adjusted", "Actual"])]

    #Analyze only Filled jobs
    df_jobs = df[df['Series_title_1'] == "Filled jobs"]
    df_earnings = df[df['Series_title_1'] == "Total earnings"]  

    #grouped = df.groupby(['Period', data_col])['Data_value'].mean().unstack()
    #top_categories = grouped.mean().sort_values(ascending=False).head(5).index
    #grouped = grouped[top_categories]
    jobs_grouped = df_jobs.groupby('Period')['Data_value'].mean()
    earnings_grouped = df_earnings.groupby('Period')['Data_value'].mean()

    #Normalization
    jobs_norm = (jobs_grouped - jobs_grouped.min()) / (jobs_grouped.max() - jobs_grouped.min())
    earnings_norm = (earnings_grouped - earnings_grouped.min()) / (earnings_grouped.max() - earnings_grouped.min())

    combined = pd.concat([jobs_norm, earnings_norm], axis=1)
    combined.columns = ["Jobs", "Earnings"]
    combined = combined.dropna() 

    plt.figure()
    plt.plot(combined.index, combined["Jobs"], label="Jobs")
    plt.plot(combined.index, combined["Earnings"], label="Earnings")
    plt.legend()    

    plt.title(f"{category.capitalize()} Analysis Over Time")
    plt.xlabel("Period")
    plt.ylabel("Normalized data values")
    plot_path = f"{category}_normalized_plot_.png"
    plt.savefig(plot_path)
    plt.close()

    summary = {
        "jobs_mean": float(jobs_grouped.mean()),
        "earnings_mean": float(earnings_grouped.mean())
    }    
    return summary, plot_path