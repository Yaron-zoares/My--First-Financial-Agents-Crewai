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
    
    # Calculate NPV with 6% discount rate using correct formula
    # NPV = \sum_{t=1}^{n} \frac{CF_t}{(1 + r)^t}
    df = df.sort_values('date')  # Ensure chronological order
    df['time_period'] = range(1, len(df) + 1)  # t = 1, 2, 3, ...
    df['discount_factor'] = 1 / ((1 + 0.06) ** df['time_period'])
    df['npv_net_profit'] = df['net_profit_after_tax'] * df['discount_factor']
    
    return df

def calculate_correct_npv(cash_flows, discount_rate=0.06):
    """Calculate NPV using the correct standard formula"""
    npv = 0
    for t, cf in enumerate(cash_flows, 1):
        npv += cf / ((1 + discount_rate) ** t)
    return npv

def create_monthly_forecast_table(df, months_ahead=60, export_to_file=True):
    """Create detailed monthly forecast table with revenue and cost projections"""
    
    print("\n📅 MONTHLY FORECAST TABLE - טבלת תחזית חודשית")
    print("="*80)
    
    # Calculate growth rates from historical data
    monthly_data = df.groupby(df['date'].dt.to_period('M')).agg({
        'revenue': 'sum',
        'opex': 'sum',
        'tax': 'sum',
        'fianance cost': 'sum',
        'sg@a': 'sum',
        'net_profit_after_tax': 'sum'
    })
    
    # Calculate monthly growth rates
    revenue_growth_rate = (monthly_data['revenue'].iloc[-1] / monthly_data['revenue'].iloc[0]) ** (1/len(monthly_data)) - 1
    opex_growth_rate = (monthly_data['opex'].iloc[-1] / monthly_data['opex'].iloc[0]) ** (1/len(monthly_data)) - 1
    tax_growth_rate = (monthly_data['tax'].iloc[-1] / monthly_data['tax'].iloc[0]) ** (1/len(monthly_data)) - 1
    finance_growth_rate = (monthly_data['fianance cost'].iloc[-1] / monthly_data['fianance cost'].iloc[0]) ** (1/len(monthly_data)) - 1
    sga_growth_rate = (monthly_data['sg@a'].iloc[-1] / monthly_data['sg@a'].iloc[0]) ** (1/len(monthly_data)) - 1
    
    # Get last month's values as baseline
    last_month_revenue = monthly_data['revenue'].iloc[-1]
    last_month_opex = monthly_data['opex'].iloc[-1]
    last_month_tax = monthly_data['tax'].iloc[-1]
    last_month_finance = monthly_data['fianance cost'].iloc[-1]
    last_month_sga = monthly_data['sg@a'].iloc[-1]
    
    # Create forecast scenarios
    scenarios = {
        'Conservative': {
            'revenue_growth': revenue_growth_rate * 0.5,
            'opex_growth': opex_growth_rate * 0.5,
            'tax_growth': tax_growth_rate * 0.5,
            'finance_growth': finance_growth_rate * 0.5,
            'sga_growth': sga_growth_rate * 0.5
        },
        'Moderate': {
            'revenue_growth': revenue_growth_rate,
            'opex_growth': opex_growth_rate,
            'tax_growth': tax_growth_rate,
            'finance_growth': finance_growth_rate,
            'sga_growth': sga_growth_rate
        },
        'Optimistic': {
            'revenue_growth': revenue_growth_rate * 1.5,
            'opex_growth': opex_growth_rate * 1.5,
            'tax_growth': tax_growth_rate * 1.5,
            'finance_growth': finance_growth_rate * 1.5,
            'sga_growth': sga_growth_rate * 1.5
        }
    }
    
    # Dictionary to store all forecast data for export
    all_forecast_data = {}
    
    # Generate forecast for each scenario
    for scenario_name, growth_rates in scenarios.items():
        print(f"\n🎯 {scenario_name.upper()} SCENARIO - תרחיש {scenario_name}")
        print("-" * 80)
        
        # Header
        print(f"{'Month':<12} {'Revenue':<12} {'OPEX':<12} {'Tax':<12} {'Finance':<12} {'SG&A':<12} {'Net Profit':<12} {'Margin':<10}")
        print("-" * 100)
        
        # Lists to store forecast data for this scenario
        forecast_months = []
        forecast_revenues = []
        forecast_opex = []
        forecast_tax = []
        forecast_finance = []
        forecast_sga = []
        forecast_net_profit = []
        forecast_margin = []
        
        # Calculate and display monthly forecasts
        current_revenue = last_month_revenue
        current_opex = last_month_opex
        current_tax = last_month_tax
        current_finance = last_month_finance
        current_sga = last_month_sga
        
        # Get the last date from historical data
        last_date = df['date'].max()
        
        for month_num in range(1, months_ahead + 1):
            # Calculate next month's date
            forecast_date = last_date + pd.DateOffset(months=month_num)
            month_label = forecast_date.strftime('%b-%Y')
            
            # Calculate forecasted values
            forecast_revenue = current_revenue * (1 + growth_rates['revenue_growth'])
            forecast_opex_val = current_opex * (1 + growth_rates['opex_growth'])
            forecast_tax_val = current_tax * (1 + growth_rates['tax_growth'])
            forecast_finance_val = current_finance * (1 + growth_rates['finance_growth'])
            forecast_sga_val = current_sga * (1 + growth_rates['sga_growth'])
            
            # Calculate net profit
            forecast_net_profit_val = forecast_revenue - forecast_opex_val - forecast_tax_val - forecast_finance_val - forecast_sga_val
            
            # Calculate profit margin
            forecast_margin_val = (forecast_net_profit_val / forecast_revenue * 100) if forecast_revenue > 0 else 0
            
            # Store data for export
            forecast_months.append(month_label)
            forecast_revenues.append(forecast_revenue)
            forecast_opex.append(forecast_opex_val)
            forecast_tax.append(forecast_tax_val)
            forecast_finance.append(forecast_finance_val)
            forecast_sga.append(forecast_sga_val)
            forecast_net_profit.append(forecast_net_profit_val)
            forecast_margin.append(forecast_margin_val)
            
            # Display the forecast
            print(f"{month_label:<12} ${forecast_revenue:<11,.0f} ${forecast_opex_val:<11,.0f} ${forecast_tax_val:<11,.0f} "
                  f"${forecast_finance_val:<11,.0f} ${forecast_sga_val:<11,.0f} ${forecast_net_profit_val:<11,.0f} {forecast_margin_val:<9.1f}%")
            
            # Update current values for next iteration
            current_revenue = forecast_revenue
            current_opex = forecast_opex_val
            current_tax = forecast_tax_val
            current_finance = forecast_finance_val
            current_sga = forecast_sga_val
        
        # Summary for this scenario
        total_forecast_revenue = sum([last_month_revenue * ((1 + growth_rates['revenue_growth']) ** i) for i in range(1, months_ahead + 1)])
        total_forecast_profit = sum([(last_month_revenue * ((1 + growth_rates['revenue_growth']) ** i) - 
                                   (last_month_opex * ((1 + growth_rates['opex_growth']) ** i) +
                                    last_month_tax * ((1 + growth_rates['tax_growth']) ** i) +
                                    last_month_finance * ((1 + growth_rates['finance_growth']) ** i) +
                                    last_month_sga * ((1 + growth_rates['sga_growth']) ** i))) for i in range(1, months_ahead + 1)])
        
        print("-" * 100)
        print(f"📊 {scenario_name} Scenario Summary:")
        print(f"   Total Forecast Revenue: ${total_forecast_revenue:,.2f}")
        print(f"   Total Forecast Profit: ${total_forecast_profit:,.2f}")
        print(f"   Average Monthly Revenue: ${total_forecast_revenue/months_ahead:,.2f}")
        print(f"   Average Monthly Profit: ${total_forecast_profit/months_ahead:,.2f}")
        
        # Store scenario data for export
        all_forecast_data[scenario_name] = {
            'Month': forecast_months,
            'Revenue': forecast_revenues,
            'OPEX': forecast_opex,
            'Tax': forecast_tax,
            'Finance_Cost': forecast_finance,
            'SG&A': forecast_sga,
            'Net_Profit': forecast_net_profit,
            'Profit_Margin_%': forecast_margin,
            'Total_Revenue': total_forecast_revenue,
            'Total_Profit': total_forecast_profit,
            'Avg_Monthly_Revenue': total_forecast_revenue/months_ahead,
            'Avg_Monthly_Profit': total_forecast_profit/months_ahead
        }
    
    # Export to files if requested
    if export_to_file:
        export_forecast_data(all_forecast_data, months_ahead)
    
    return all_forecast_data

def export_forecast_data(all_forecast_data, months_ahead):
    """Export forecast data to CSV and Excel files"""
    
    try:
        # Create timestamp for file names
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Export each scenario to separate CSV files
        for scenario_name, data in all_forecast_data.items():
            # Create DataFrame for monthly data
            monthly_df = pd.DataFrame({
                'Month': data['Month'],
                'Revenue': data['Revenue'],
                'OPEX': data['OPEX'],
                'Tax': data['Tax'],
                'Finance_Cost': data['Finance_Cost'],
                'SG&A': data['SG&A'],
                'Net_Profit': data['Net_Profit'],
                'Profit_Margin_%': data['Profit_Margin_%']
            })
            
            # Create summary DataFrame
            summary_df = pd.DataFrame({
                'Metric': ['Total_Revenue', 'Total_Profit', 'Avg_Monthly_Revenue', 'Avg_Monthly_Profit'],
                'Value': [data['Total_Revenue'], data['Total_Profit'], 
                         data['Avg_Monthly_Revenue'], data['Avg_Monthly_Profit']]
            })
            
            # Export to CSV
            csv_filename = f"forecast_{scenario_name.lower()}_{months_ahead}months_{timestamp}.csv"
            monthly_df.to_csv(csv_filename, index=False)
            print(f"✅ Exported {scenario_name} forecast to: {csv_filename}")
            
            # Export summary to separate CSV
            summary_csv_filename = f"forecast_{scenario_name.lower()}_summary_{timestamp}.csv"
            summary_df.to_csv(summary_csv_filename, index=False)
            print(f"✅ Exported {scenario_name} summary to: {summary_csv_filename}")
        
        # Create comprehensive Excel file with all scenarios
        excel_filename = f"comprehensive_forecast_{months_ahead}months_{timestamp}.xlsx"
        
        with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
            # Write each scenario to a separate sheet
            for scenario_name, data in all_forecast_data.items():
                # Monthly data sheet
                monthly_df = pd.DataFrame({
                    'Month': data['Month'],
                    'Revenue': data['Revenue'],
                    'OPEX': data['OPEX'],
                    'Tax': data['Tax'],
                    'Finance_Cost': data['Finance_Cost'],
                    'SG&A': data['SG&A'],
                    'Net_Profit': data['Net_Profit'],
                    'Profit_Margin_%': data['Profit_Margin_%']
                })
                monthly_df.to_excel(writer, sheet_name=f'{scenario_name}_Monthly', index=False)
                
                # Summary sheet
                summary_df = pd.DataFrame({
                    'Metric': ['Total_Revenue', 'Total_Profit', 'Avg_Monthly_Revenue', 'Avg_Monthly_Profit'],
                    'Value': [data['Total_Revenue'], data['Total_Profit'], 
                             data['Avg_Monthly_Revenue'], data['Avg_Monthly_Profit']]
                })
                summary_df.to_excel(writer, sheet_name=f'{scenario_name}_Summary', index=False)
            
            # Create comparison sheet
            comparison_data = []
            for scenario_name, data in all_forecast_data.items():
                comparison_data.append({
                    'Scenario': scenario_name,
                    'Total_Revenue': data['Total_Revenue'],
                    'Total_Profit': data['Total_Profit'],
                    'Avg_Monthly_Revenue': data['Avg_Monthly_Revenue'],
                    'Avg_Monthly_Profit': data['Avg_Monthly_Profit']
                })
            
            comparison_df = pd.DataFrame(comparison_data)
            comparison_df.to_excel(writer, sheet_name='Scenario_Comparison', index=False)
        
        print(f"✅ Exported comprehensive Excel file: {excel_filename}")
        print(f"📊 Files contain {months_ahead} months of forecast data for all scenarios")
        
    except Exception as e:
        print(f"❌ Error exporting forecast data: {str(e)}")
        print("📝 Forecast data is still available in the console output")

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
    
    # 4. NPV Analysis with correct formula
    print("\n💰 NPV ANALYSIS (6% Discount Rate) - CORRECTED FORMULA:")
    print("-" * 50)
    
    # Calculate NPV using the correct formula
    cash_flows = df['net_profit_after_tax'].values
    correct_npv = calculate_correct_npv(cash_flows, discount_rate=0.06)
    
    print(f"Total NPV (corrected formula):    ${correct_npv:>15,.2f}")
    print(f"Previous NPV calculation:         ${total_npv:>15,.2f}")
    print(f"Difference:                       ${correct_npv - total_npv:>15,.2f}")
    print(f"NPV as % of total profit:         {(correct_npv/total_profit)*100:>15.1f}%")
    print(f"Discount rate applied:            {6:>15.0f}%")
    print(f"Formula used: NPV = Σ(CF_t / (1 + r)^t)")
    
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
    
    # 10. Monthly Forecast Table (NEW)
    create_monthly_forecast_table(df, months_ahead=60, export_to_file=True)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETED SUCCESSFULLY")
    print("="*80)

if __name__ == "__main__":
    # Load and analyze data
    print("Loading financial data...")
    financial_df = load_and_analyze_data('agent_test.csv')
    
    # Display detailed results
    display_detailed_results(financial_df) 