# Financial Visualization Script
# סקריפט יצירת גרפים פיננסיים מקצועיים

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import matplotlib.dates as mdates

# Set style for professional charts
plt.style.use('seaborn-v0_8')
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

def load_and_prepare_data(csv_file_path):
    """Load financial data from CSV file and prepare for analysis"""
    try:
        # Read CSV file
        df = pd.read_csv(csv_file_path)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Remove empty rows
        df = df.dropna(subset=['revenue'])
        
        # Convert date column
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
        
        print(f"✅ Data loaded successfully: {len(df)} records")
        print(f"📊 Date range: {df['date'].min().strftime('%Y-%m')} to {df['date'].max().strftime('%Y-%m')}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error loading data: {str(e)}")
        raise

def create_comprehensive_dashboard(df):
    """Create comprehensive financial dashboard with multiple charts"""
    
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 16))
    
    # Create grid layout
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Main title
    fig.suptitle('Financial Analysis Dashboard - דשבורד ניתוח פיננסי', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # 1. Revenue and Net Profit Over Time (top left)
    ax1 = fig.add_subplot(gs[0, :2])
    ax1.plot(df['date'], df['revenue'], 'b-', label='Revenue - הכנסות', linewidth=2, marker='o')
    ax1.plot(df['date'], df['net_profit_after_tax'], 'g-', label='Net Profit - רווח נקי', linewidth=2, marker='s')
    ax1.set_title('Revenue vs Net Profit Over Time\nהכנסות מול רווח נקי לאורך זמן')
    ax1.set_xlabel('Date - תאריך')
    ax1.set_ylabel('Amount (USD) - סכום (דולר)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # 2. Profit Margin Trend (top right)
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.plot(df['date'], df['profit_margin'], 'r-', linewidth=2, marker='o')
    ax2.set_title('Profit Margin Trend\nמגמת שולי רווח')
    ax2.set_xlabel('Date - תאריך')
    ax2.set_ylabel('Profit Margin (%) - שולי רווח (%)')
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='x', rotation=45)
    
    # 3. Quarterly Revenue Breakdown (middle left)
    ax3 = fig.add_subplot(gs[1, 0])
    quarterly_revenue = df.groupby('quarter_label')['revenue'].sum()
    bars = ax3.bar(range(len(quarterly_revenue)), quarterly_revenue.values, color='skyblue', alpha=0.7)
    ax3.set_title('Quarterly Revenue Breakdown\nפילוח הכנסות לפי רבעונים')
    ax3.set_xlabel('Quarter - רבעון')
    ax3.set_ylabel('Revenue (USD) - הכנסות (דולר)')
    ax3.set_xticks(range(len(quarterly_revenue)))
    ax3.set_xticklabels(quarterly_revenue.index, rotation=45)
    
    # Add value labels on bars
    for bar, value in zip(bars, quarterly_revenue.values):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(quarterly_revenue.values)*0.01,
                f'${value:,.0f}', ha='center', va='bottom', fontsize=8)
    
    # 4. Net Profit After Tax by Quarter (middle center)
    ax4 = fig.add_subplot(gs[1, 1])
    quarterly_profit = df.groupby('quarter_label')['net_profit_after_tax'].sum()
    bars = ax4.bar(range(len(quarterly_profit)), quarterly_profit.values, color='lightgreen', alpha=0.7)
    ax4.set_title('Net Profit After Tax by Quarter\nרווח נקי לאחר מס לפי רבעון')
    ax4.set_xlabel('Quarter - רבעון')
    ax4.set_ylabel('Net Profit (USD) - רווח נקי (דולר)')
    ax4.set_xticks(range(len(quarterly_profit)))
    ax4.set_xticklabels(quarterly_profit.index, rotation=45)
    
    # Add value labels on bars
    for bar, value in zip(bars, quarterly_profit.values):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(quarterly_profit.values)*0.01,
                f'${value:,.0f}', ha='center', va='bottom', fontsize=8)
    
    # 5. NPV Analysis (middle right)
    ax5 = fig.add_subplot(gs[1, 2])
    ax5.plot(df['date'], df['npv_net_profit'], 'purple', linewidth=2, marker='o')
    ax5.set_title('NPV of Net Profit (6% Discount)\nערך נוכחי של רווח נקי (6% היוון)')
    ax5.set_xlabel('Date - תאריך')
    ax5.set_ylabel('NPV (USD) - ערך נוכחי (דולר)')
    ax5.grid(True, alpha=0.3)
    ax5.tick_params(axis='x', rotation=45)
    
    # 6. Monthly Performance Heatmap (bottom left)
    ax6 = fig.add_subplot(gs[2, 0])
    monthly_data = df.pivot_table(values='revenue', index=df['date'].dt.year, 
                                 columns=df['date'].dt.month, aggfunc='sum')
    sns.heatmap(monthly_data, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax6)
    ax6.set_title('Monthly Revenue Heatmap\nמפת חום הכנסות חודשיות')
    ax6.set_xlabel('Month - חודש')
    ax6.set_ylabel('Year - שנה')
    
    # 7. Cost Structure Analysis (bottom center)
    ax7 = fig.add_subplot(gs[2, 1])
    cost_columns = ['opex', 'tax', 'fianance cost', 'sg@a']
    cost_labels = ['Operating Expenses', 'Tax', 'Finance Cost', 'SG&A']
    avg_costs = [df[col].mean() for col in cost_columns]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    wedges, texts, autotexts = ax7.pie(avg_costs, labels=cost_labels, autopct='%1.1f%%', 
                                       colors=colors, startangle=90)
    ax7.set_title('Average Cost Structure\nמבנה עלויות ממוצע')
    
    # 8. Growth Rate Analysis (bottom right)
    ax8 = fig.add_subplot(gs[2, 2])
    df['revenue_growth'] = df['revenue'].pct_change() * 100
    df['profit_growth'] = df['net_profit_after_tax'].pct_change() * 100
    
    ax8.plot(df['date'], df['revenue_growth'], 'b-', label='Revenue Growth', linewidth=2, marker='o')
    ax8.plot(df['date'], df['profit_growth'], 'g-', label='Profit Growth', linewidth=2, marker='s')
    ax8.set_title('Growth Rate Analysis\nניתוח קצב צמיחה')
    ax8.set_xlabel('Date - תאריך')
    ax8.set_ylabel('Growth Rate (%) - קצב צמיחה (%)')
    ax8.legend()
    ax8.grid(True, alpha=0.3)
    ax8.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    return df

def print_financial_summary(df):
    """Print comprehensive financial summary"""
    
    print("\n" + "="*80)
    print("📊 COMPREHENSIVE FINANCIAL ANALYSIS - ניתוח פיננסי מקיף")
    print("="*80)
    
    # Key Metrics
    total_revenue = df['revenue'].sum()
    total_profit = df['net_profit_after_tax'].sum()
    total_npv = df['npv_net_profit'].sum()
    avg_profit_margin = df['profit_margin'].mean()
    
    print(f"\n💰 KEY METRICS - מדדים מרכזיים:")
    print(f"   Total Revenue: ${total_revenue:,.2f}")
    print(f"   Total Net Profit After Tax: ${total_profit:,.2f}")
    print(f"   Total NPV (6% discount): ${total_npv:,.2f}")
    print(f"   Average Profit Margin: {avg_profit_margin:.2f}%")
    
    # Quarterly Analysis
    print(f"\n📈 QUARTERLY ANALYSIS - ניתוח רבעוני:")
    quarterly_summary = df.groupby('quarter_label').agg({
        'revenue': 'sum',
        'net_profit_after_tax': 'sum',
        'npv_net_profit': 'sum'
    }).round(2)
    
    print(quarterly_summary.to_string())
    
    # Growth Analysis
    print(f"\n📊 GROWTH ANALYSIS - ניתוח צמיחה:")
    revenue_growth = ((df['revenue'].iloc[-1] - df['revenue'].iloc[0]) / df['revenue'].iloc[0]) * 100
    profit_growth = ((df['net_profit_after_tax'].iloc[-1] - df['net_profit_after_tax'].iloc[0]) / df['net_profit_after_tax'].iloc[0]) * 100
    
    print(f"   Revenue Growth: {revenue_growth:.2f}%")
    print(f"   Profit Growth: {profit_growth:.2f}%")
    
    # Best and Worst Performers
    print(f"\n🏆 PERFORMANCE HIGHLIGHTS - נקודות ציון ביצועים:")
    best_month_revenue = df.loc[df['revenue'].idxmax()]
    worst_month_revenue = df.loc[df['revenue'].idxmin()]
    best_month_profit = df.loc[df['net_profit_after_tax'].idxmax()]
    worst_month_profit = df.loc[df['net_profit_after_tax'].idxmin()]
    
    print(f"   Best Revenue Month: {best_month_revenue['monthes']} (${best_month_revenue['revenue']:,.2f})")
    print(f"   Worst Revenue Month: {worst_month_revenue['monthes']} (${worst_month_revenue['revenue']:,.2f})")
    print(f"   Best Profit Month: {best_month_profit['monthes']} (${best_month_profit['net_profit_after_tax']:,.2f})")
    print(f"   Worst Profit Month: {worst_month_profit['monthes']} (${worst_month_profit['net_profit_after_tax']:,.2f})")
    
    print("\n" + "="*80)

def create_forecast_analysis(df):
    """Create 5-year forecast analysis"""
    
    print("\n🔮 5-YEAR FORECAST ANALYSIS - ניתוח תחזית לחמש שנים")
    print("="*60)
    
    # Simple trend-based forecast
    # Calculate average quarterly growth
    quarterly_data = df.groupby('quarter_label').agg({
        'revenue': 'sum',
        'net_profit_after_tax': 'sum'
    })
    
    # Calculate growth rates
    revenue_growth_rate = (quarterly_data['revenue'].iloc[-1] / quarterly_data['revenue'].iloc[0]) ** (1/len(quarterly_data)) - 1
    profit_growth_rate = (quarterly_data['net_profit_after_tax'].iloc[-1] / quarterly_data['net_profit_after_tax'].iloc[0]) ** (1/len(quarterly_data)) - 1
    
    print(f"📈 Calculated Growth Rates:")
    print(f"   Revenue Growth Rate per Quarter: {revenue_growth_rate*100:.2f}%")
    print(f"   Profit Growth Rate per Quarter: {profit_growth_rate*100:.2f}%")
    
    # Create forecast scenarios
    last_quarter_revenue = quarterly_data['revenue'].iloc[-1]
    last_quarter_profit = quarterly_data['net_profit_after_tax'].iloc[-1]
    
    print(f"\n🎯 FORECAST SCENARIOS - תרחישי תחזית:")
    
    # Conservative scenario (50% of calculated growth)
    conservative_revenue_growth = revenue_growth_rate * 0.5
    conservative_profit_growth = profit_growth_rate * 0.5
    
    # Optimistic scenario (150% of calculated growth)
    optimistic_revenue_growth = revenue_growth_rate * 1.5
    optimistic_profit_growth = profit_growth_rate * 1.5
    
    print(f"   Conservative Scenario:")
    print(f"     Revenue Growth: {conservative_revenue_growth*100:.2f}% per quarter")
    print(f"     Profit Growth: {conservative_profit_growth*100:.2f}% per quarter")
    
    print(f"   Moderate Scenario:")
    print(f"     Revenue Growth: {revenue_growth_rate*100:.2f}% per quarter")
    print(f"     Profit Growth: {profit_growth_rate*100:.2f}% per quarter")
    
    print(f"   Optimistic Scenario:")
    print(f"     Revenue Growth: {optimistic_revenue_growth*100:.2f}% per quarter")
    print(f"     Profit Growth: {optimistic_profit_growth*100:.2f}% per quarter")
    
    # Calculate 5-year projections
    quarters_5_years = 20  # 5 years * 4 quarters
    
    print(f"\n📊 5-YEAR PROJECTIONS - תחזיות לחמש שנים:")
    
    # Conservative
    conservative_revenue_5y = last_quarter_revenue * ((1 + conservative_revenue_growth) ** quarters_5_years)
    conservative_profit_5y = last_quarter_profit * ((1 + conservative_profit_growth) ** quarters_5_years)
    
    # Moderate
    moderate_revenue_5y = last_quarter_revenue * ((1 + revenue_growth_rate) ** quarters_5_years)
    moderate_profit_5y = last_quarter_profit * ((1 + profit_growth_rate) ** quarters_5_years)
    
    # Optimistic
    optimistic_revenue_5y = last_quarter_revenue * ((1 + optimistic_revenue_growth) ** quarters_5_years)
    optimistic_profit_5y = last_quarter_profit * ((1 + optimistic_profit_growth) ** quarters_5_years)
    
    print(f"   Conservative 5-Year Revenue: ${conservative_revenue_5y:,.2f}")
    print(f"   Conservative 5-Year Profit: ${conservative_profit_5y:,.2f}")
    print(f"   Moderate 5-Year Revenue: ${moderate_revenue_5y:,.2f}")
    print(f"   Moderate 5-Year Profit: ${moderate_profit_5y:,.2f}")
    print(f"   Optimistic 5-Year Revenue: ${optimistic_revenue_5y:,.2f}")
    print(f"   Optimistic 5-Year Profit: ${optimistic_profit_5y:,.2f}")

if __name__ == "__main__":
    # Load and prepare data
    print("🚀 Loading financial data...")
    financial_df = load_and_prepare_data('agent_test.csv')
    
    # Create comprehensive dashboard
    print("\n📊 Creating comprehensive financial dashboard...")
    enhanced_df = create_comprehensive_dashboard(financial_df)
    
    # Print financial summary
    print_financial_summary(enhanced_df)
    
    # Create forecast analysis
    create_forecast_analysis(enhanced_df)
    
    print("\n✅ Analysis completed successfully!")
    print("📈 All visualizations and analysis have been generated.") 