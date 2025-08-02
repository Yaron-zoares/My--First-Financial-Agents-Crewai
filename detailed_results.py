# Detailed Financial Results Display
# הצגת תוצאות פיננסיות מפורטות

import pandas as pd
import numpy as np
from datetime import datetime

def load_and_analyze_data(csv_file_path):
    """Load and analyze financial data with detailed calculations"""
    
    # Load data
    df = pd.read_csv(csv_file_path)
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=['revenue'])
    df['date'] = pd.to_datetime(df['monthes'], format='%b-%y')
    
    # Calculate net profit after tax
    df['net_profit_after_tax'] = df['revenue'] - df['opex'] - df['tax'] - df['fianance cost'] - df['sg@a']
    
    # Add quarter information
    df['quarter'] = df['date'].dt.quarter
    df['year'] = df['date'].dt.year
    df['quarter_label'] = 'Q' + df['quarter'].astype(str) + '-' + df['year'].astype(str)
    
    # Calculate profit margin
    df['profit_margin'] = (df['net_profit_after_tax'] / df['revenue']) * 100
    
    # Calculate NPV with 6% discount rate
    df['quarter_number'] = (df['date'].dt.year - df['date'].dt.year.min()) * 4 + df['date'].dt.quarter
    df['discount_factor'] = 1 / ((1 + 0.06) ** (df['quarter_number'] / 4))
    df['npv_net_profit'] = df['net_profit_after_tax'] * df['discount_factor']
    
    return df

def display_detailed_results(df):
    """Display comprehensive financial analysis results"""
    
    print("="*80)
    print("FINANCIAL ANALYSIS RESULTS - תוצאות ניתוח פיננסי")
    print("="*80)
    
    # 1. Key Metrics
    print("\n📊 KEY FINANCIAL METRICS:")
    print("-" * 50)
    
    total_revenue = df['revenue'].sum()
    total_profit = df['net_profit_after_tax'].sum()
    total_npv = df['npv_net_profit'].sum()
    avg_profit_margin = df['profit_margin'].mean()
    
    print(f"Total Revenue:                    ${total_revenue:>15,.2f}")
    print(f"Total Net Profit After Tax:       ${total_profit:>15,.2f}")
    print(f"Total NPV (6% discount):          ${total_npv:>15,.2f}")
    print(f"Average Profit Margin:            {avg_profit_margin:>15.2f}%")
    print(f"Number of Records:                {len(df):>15}")
    print(f"Date Range:                       {df['date'].min().strftime('%Y-%m'):>15} to {df['date'].max().strftime('%Y-%m'):>15}")
    
    # 2. Quarterly Analysis
    print("\n📈 QUARTERLY PERFORMANCE ANALYSIS:")
    print("-" * 50)
    
    quarterly_summary = df.groupby('quarter_label').agg({
        'revenue': 'sum',
        'net_profit_after_tax': 'sum',
        'npv_net_profit': 'sum'
    }).round(2)
    
    print(f"{'Quarter':<12} {'Revenue':<15} {'Net Profit':<15} {'NPV':<15}")
    print("-" * 60)
    
    for quarter in quarterly_summary.index:
        revenue = quarterly_summary.loc[quarter, 'revenue']
        profit = quarterly_summary.loc[quarter, 'net_profit_after_tax']
        npv = quarterly_summary.loc[quarter, 'npv_net_profit']
        print(f"{quarter:<12} ${revenue:<14,.0f} ${profit:<14,.0f} ${npv:<14,.0f}")
    
    # 3. Monthly Detailed Analysis
    print("\n📅 MONTHLY DETAILED ANALYSIS:")
    print("-" * 50)
    
    print(f"{'Month':<12} {'Revenue':<12} {'OPEX':<12} {'Tax':<12} {'Finance':<12} {'SG&A':<12} {'Net Profit':<12} {'Margin':<10}")
    print("-" * 100)
    
    for _, row in df.iterrows():
        month = row['monthes']
        revenue = row['revenue']
        opex = row['opex']
        tax = row['tax']
        finance = row['fianance cost']
        sga = row['sg@a']
        net_profit = row['net_profit_after_tax']
        margin = row['profit_margin']
        
        print(f"{month:<12} ${revenue:<11,.0f} ${opex:<11,.0f} ${tax:<11,.0f} ${finance:<11,.0f} ${sga:<11,.0f} ${net_profit:<11,.0f} {margin:<9.1f}%")
    
    # 4. NPV Analysis
    print("\n💰 NPV ANALYSIS (6% Discount Rate):")
    print("-" * 50)
    
    print(f"Total NPV of all profits:         ${total_npv:>15,.2f}")
    print(f"Average quarterly NPV:            ${df['npv_net_profit'].mean():>15,.2f}")
    print(f"NPV as % of total profit:         {(total_npv/total_profit)*100:>15.1f}%")
    print(f"Discount rate applied:            {6:>15.0f}%")
    
    # 5. Performance Highlights
    print("\n🏆 PERFORMANCE HIGHLIGHTS:")
    print("-" * 50)
    
    best_revenue_month = df.loc[df['revenue'].idxmax()]
    worst_revenue_month = df.loc[df['revenue'].idxmin()]
    best_profit_month = df.loc[df['net_profit_after_tax'].idxmax()]
    worst_profit_month = df.loc[df['net_profit_after_tax'].idxmin()]
    
    print(f"Best Revenue Month:               {best_revenue_month['monthes']:<15} (${best_revenue_month['revenue']:,.2f})")
    print(f"Worst Revenue Month:              {worst_revenue_month['monthes']:<15} (${worst_revenue_month['revenue']:,.2f})")
    print(f"Best Profit Month:                {best_profit_month['monthes']:<15} (${best_profit_month['net_profit_after_tax']:,.2f})")
    print(f"Worst Profit Month:               {worst_profit_month['monthes']:<15} (${worst_profit_month['net_profit_after_tax']:,.2f})")
    
    # 6. Growth Analysis
    print("\n📊 GROWTH ANALYSIS:")
    print("-" * 50)
    
    revenue_growth = ((df['revenue'].iloc[-1] - df['revenue'].iloc[0]) / df['revenue'].iloc[0]) * 100
    profit_growth = ((df['net_profit_after_tax'].iloc[-1] - df['net_profit_after_tax'].iloc[0]) / df['net_profit_after_tax'].iloc[0]) * 100
    
    print(f"Revenue Growth (start to end):    {revenue_growth:>15.2f}%")
    print(f"Profit Growth (start to end):     {profit_growth:>15.2f}%")
    print(f"Average Monthly Revenue:          ${df['revenue'].mean():>15,.2f}")
    print(f"Average Monthly Profit:           ${df['net_profit_after_tax'].mean():>15,.2f}")
    
    # 7. Cost Structure Analysis
    print("\n💼 COST STRUCTURE ANALYSIS:")
    print("-" * 50)
    
    total_opex = df['opex'].sum()
    total_tax = df['tax'].sum()
    total_finance = df['fianance cost'].sum()
    total_sga = df['sg@a'].sum()
    
    print(f"Total Operating Expenses:         ${total_opex:>15,.2f} ({total_opex/total_revenue*100:.1f}%)")
    print(f"Total Tax:                        ${total_tax:>15,.2f} ({total_tax/total_revenue*100:.1f}%)")
    print(f"Total Finance Cost:               ${total_finance:>15,.2f} ({total_finance/total_revenue*100:.1f}%)")
    print(f"Total SG&A:                       ${total_sga:>15,.2f} ({total_sga/total_revenue*100:.1f}%)")
    print(f"Total Costs:                      ${total_opex + total_tax + total_finance + total_sga:>15,.2f}")
    print(f"Net Profit:                       ${total_profit:>15,.2f} ({total_profit/total_revenue*100:.1f}%)")
    
    # 8. Statistical Summary
    print("\n📈 STATISTICAL SUMMARY:")
    print("-" * 50)
    
    print(f"Revenue Statistics:")
    print(f"  Mean:                           ${df['revenue'].mean():>15,.2f}")
    print(f"  Median:                         ${df['revenue'].median():>15,.2f}")
    print(f"  Standard Deviation:             ${df['revenue'].std():>15,.2f}")
    print(f"  Minimum:                        ${df['revenue'].min():>15,.2f}")
    print(f"  Maximum:                        ${df['revenue'].max():>15,.2f}")
    
    print(f"\nProfit Statistics:")
    print(f"  Mean:                           ${df['net_profit_after_tax'].mean():>15,.2f}")
    print(f"  Median:                         ${df['net_profit_after_tax'].median():>15,.2f}")
    print(f"  Standard Deviation:             ${df['net_profit_after_tax'].std():>15,.2f}")
    print(f"  Minimum:                        ${df['net_profit_after_tax'].min():>15,.2f}")
    print(f"  Maximum:                        ${df['net_profit_after_tax'].max():>15,.2f}")
    
    # 9. Forecast Analysis
    print("\n🔮 FORECAST ANALYSIS:")
    print("-" * 50)
    
    quarterly_data = df.groupby('quarter_label').agg({
        'revenue': 'sum',
        'net_profit_after_tax': 'sum'
    })
    
    revenue_growth_rate = (quarterly_data['revenue'].iloc[-1] / quarterly_data['revenue'].iloc[0]) ** (1/len(quarterly_data)) - 1
    profit_growth_rate = (quarterly_data['net_profit_after_tax'].iloc[-1] / quarterly_data['net_profit_after_tax'].iloc[0]) ** (1/len(quarterly_data)) - 1
    
    print(f"Revenue Growth Rate per Quarter:  {revenue_growth_rate*100:>15.2f}%")
    print(f"Profit Growth Rate per Quarter:   {profit_growth_rate*100:>15.2f}%")
    
    # 5-year projections
    quarters_5_years = 20
    last_quarter_revenue = quarterly_data['revenue'].iloc[-1]
    last_quarter_profit = quarterly_data['net_profit_after_tax'].iloc[-1]
    
    conservative_revenue = last_quarter_revenue * ((1 + revenue_growth_rate * 0.5) ** quarters_5_years)
    moderate_revenue = last_quarter_revenue * ((1 + revenue_growth_rate) ** quarters_5_years)
    optimistic_revenue = last_quarter_revenue * ((1 + revenue_growth_rate * 1.5) ** quarters_5_years)
    
    conservative_profit = last_quarter_profit * ((1 + profit_growth_rate * 0.5) ** quarters_5_years)
    moderate_profit = last_quarter_profit * ((1 + profit_growth_rate) ** quarters_5_years)
    optimistic_profit = last_quarter_profit * ((1 + profit_growth_rate * 1.5) ** quarters_5_years)
    
    print(f"\n5-Year Revenue Projections:")
    print(f"  Conservative:                   ${conservative_revenue:>15,.2f}")
    print(f"  Moderate:                       ${moderate_revenue:>15,.2f}")
    print(f"  Optimistic:                     ${optimistic_revenue:>15,.2f}")
    
    print(f"\n5-Year Profit Projections:")
    print(f"  Conservative:                   ${conservative_profit:>15,.2f}")
    print(f"  Moderate:                       ${moderate_profit:>15,.2f}")
    print(f"  Optimistic:                     ${optimistic_profit:>15,.2f}")
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETED SUCCESSFULLY")
    print("="*80)

if __name__ == "__main__":
    # Load and analyze data
    print("Loading financial data...")
    financial_df = load_and_analyze_data('agent_test.csv')
    
    # Display detailed results
    display_detailed_results(financial_df) 