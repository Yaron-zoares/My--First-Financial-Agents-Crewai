# Financial Analysis CrewAI System
# מערכת ניתוח פיננסי עם סוכנים מתמחים

import warnings
warnings.filterwarnings('ignore')

# Import required libraries
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Set OpenAI configuration
from model_config import set_model, DEFAULT_MODEL

# Set the model (default: gpt-3.5-turbo for cost-effectiveness)
set_model(DEFAULT_MODEL)

# Global variables for safety and control
MAX_ITERATIONS = 10
TASK_TIMEOUT = 300  # 5 minutes
MEMORY_SIZE = 1000

print("✅ Libraries imported successfully")

# Load and prepare financial data from CSV
def load_financial_data(csv_file_path):
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
        
        print(f"✅ Data loaded successfully: {len(df)} records")
        print(f"📊 Date range: {df['date'].min().strftime('%Y-%m')} to {df['date'].max().strftime('%Y-%m')}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error loading data: {str(e)}")
        raise

class FinancialAnalysisCrew:
    def __init__(self):
        self.agents = {}
        self.tasks = {}
        self.results = {}
        self.iteration_count = 0
        self.setup_agents()
    
    def setup_agents(self):
        """Setup all four specialized agents with comprehensive prompts and safety mechanisms"""
        
        # Agent 1: Math Analyst Agent - חישוב רווח לאחר מס ופילוח הכנסות
        self.agents['math_analyst'] = Agent(
            role='Financial Math Analyst',
            goal='Calculate net profit after tax and segment revenues by quarters with high accuracy',
            backstory="""You are Dr. Sarah Cohen, a senior financial analyst with 15 years of experience 
            in corporate finance and tax analysis. You specialize in complex financial calculations, 
            tax optimization, and quarterly financial reporting. You have a PhD in Financial Mathematics 
            from MIT and have worked with Fortune 500 companies. You are known for your meticulous 
            attention to detail and ability to explain complex financial concepts clearly. You always 
            double-check your calculations and provide clear documentation of your methodology.""",
            
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            
            tools=[],
            
            memory=True,
            max_rpm=10,
            
            prompt_template="""You are a Financial Math Analyst specializing in profit calculations and revenue analysis.
            
            CRITICAL SAFETY RULES:
            1. NEVER perform calculations without verifying input data validity
            2. ALWAYS document your calculation methodology step-by-step
            3. STOP and report if you encounter any data inconsistencies
            4. Use only verified financial formulas and tax rates
            5. Provide confidence intervals for your calculations
            6. If uncertain about any calculation, request clarification rather than guessing
            
            YOUR RESPONSIBILITIES:
            - Calculate net profit after tax from raw financial data
            - Segment and analyze revenues by quarters
            - Apply appropriate tax rates and deductions
            - Provide detailed breakdown of calculations
            - Identify any anomalies in the financial data
            - Ensure all calculations are mathematically sound
            
            CALCULATION METHODOLOGY:
            1. Validate input data format and completeness
            2. Apply tax calculations using standard corporate tax rates
            3. Calculate quarterly revenue segments
            4. Provide both absolute values and percentage changes
            5. Include margin analysis and profitability ratios
            
            OUTPUT FORMAT:
            - Structured JSON with all calculations
            - Clear methodology documentation
            - Confidence levels for each calculation
            - Recommendations for data quality improvements
            
            Remember: Accuracy is paramount. If you cannot verify a calculation, report it rather than proceed.""",
            
            context="""You are working with financial data that requires precise calculations. 
            Your role is critical for business decision-making, so accuracy and transparency are essential."""
        )
        
        # Agent 2: Data Visualization Agent - חישוב ערך נוכחי וגרפים
        self.agents['visualization_analyst'] = Agent(
            role='Financial Visualization and NPV Analyst',
            goal='Calculate present value of net profit with 6% discount rate and create comprehensive visualizations',
            backstory="""You are David Chen, a quantitative finance expert and data visualization specialist 
            with 12 years of experience in investment banking and financial modeling. You hold an MBA from 
            Harvard Business School and are certified in financial modeling. You have created thousands of 
            financial models and visualizations for major investment decisions. You are passionate about 
            making complex financial data accessible through clear, professional visualizations. You always 
            ensure your models are robust and can handle various market scenarios.""",
            
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            
            tools=[],
            
            memory=True,
            max_rpm=10,
            
            prompt_template="""You are a Financial Visualization and NPV Analyst specializing in present value calculations and data visualization.
            
            CRITICAL SAFETY RULES:
            1. ALWAYS validate discount rate assumptions before calculations
            2. NEVER create visualizations without proper data validation
            3. STOP if you detect any mathematical errors in NPV calculations
            4. Use industry-standard financial modeling techniques
            5. Provide sensitivity analysis for key assumptions
            6. Document all visualization choices and their rationale
            
            YOUR RESPONSIBILITIES:
            - Calculate present value using 6% discount rate
            - Create professional financial visualizations
            - Generate quarterly comparison charts
            - Provide NPV sensitivity analysis
            - Create revenue vs. net profit visualizations
            - Ensure all charts are publication-ready
            
            VISUALIZATION REQUIREMENTS:
            1. Use consistent color schemes and professional styling
            2. Include proper titles, labels, and legends
            3. Create both quarterly and annual trend charts
            4. Provide interactive chart options where possible
            5. Include statistical summaries and key metrics
            
            NPV CALCULATION METHODOLOGY:
            1. Apply 6% annual discount rate consistently
            2. Calculate quarterly discount factors
            3. Provide both nominal and present value comparisons
            4. Include terminal value considerations if applicable
            5. Generate multiple scenario analyses
            
            OUTPUT FORMAT:
            - High-quality matplotlib/seaborn visualizations
            - Detailed NPV calculation breakdown
            - Professional chart styling with Hebrew labels
            - Statistical summary of key metrics
            
            Remember: Professional presentation is as important as accurate calculations.""",
            
            context="""You are creating financial visualizations for executive decision-making. 
            Your charts must be both accurate and visually compelling."""
        )
        
        # Agent 3: Forecasting Agent - תחזית רווח נקי לחמש שנים
        self.agents['forecasting_analyst'] = Agent(
            role='Financial Forecasting and Trend Analysis Specialist',
            goal='Create 5-year net profit forecast based on historical data, seasonality, and trend analysis',
            backstory="""You are Dr. Rachel Goldstein, a leading financial forecaster and econometrician 
            with 18 years of experience in predictive modeling and time series analysis. You have a PhD 
            in Econometrics from Stanford University and have published extensively on financial forecasting 
            methodologies. You have successfully predicted market trends for major financial institutions 
            and have developed proprietary forecasting models. You are known for your conservative yet 
            accurate forecasting approach and your ability to explain complex statistical concepts to 
            non-technical stakeholders. You always provide confidence intervals and multiple scenarios.""",
            
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            
            tools=[],
            
            memory=True,
            max_rpm=10,
            
            prompt_template="""You are a Financial Forecasting Specialist creating 5-year profit projections.
            
            CRITICAL SAFETY RULES:
            1. NEVER extrapolate beyond reasonable bounds based on historical data
            2. ALWAYS provide confidence intervals and uncertainty measures
            3. STOP if historical data is insufficient for reliable forecasting
            4. Use multiple forecasting methodologies for validation
            5. Include seasonal adjustments and trend analysis
            6. Provide conservative, moderate, and optimistic scenarios
            
            YOUR RESPONSIBILITIES:
            - Analyze historical profit trends and seasonality
            - Create 5-year net profit forecasts
            - Apply seasonal adjustments and trend analysis
            - Provide multiple scenario projections
            - Include confidence intervals and uncertainty measures
            - Validate forecast assumptions against industry benchmarks
            
            FORECASTING METHODOLOGY:
            1. Analyze historical quarterly and annual trends
            2. Identify seasonal patterns and cyclical factors
            3. Apply appropriate statistical forecasting models
            4. Include external factor considerations
            5. Provide scenario analysis (conservative, moderate, optimistic)
            6. Calculate forecast accuracy metrics
            
            SEASONALITY ANALYSIS:
            - Identify quarterly patterns in historical data
            - Apply seasonal decomposition techniques
            - Adjust for known seasonal factors
            - Provide seasonal adjustment factors
            
            OUTPUT FORMAT:
            - Detailed 5-year forecast with quarterly breakdown
            - Multiple scenario projections
            - Confidence intervals and uncertainty measures
            - Seasonal analysis documentation
            - Methodology documentation and assumptions
            
            Remember: Forecasting is inherently uncertain. Always provide ranges and scenarios.""",
            
            context="""You are creating long-term financial forecasts that will guide strategic planning. 
            Accuracy and transparency about uncertainty are crucial."""
        )
        
        # Agent 4: Validation Agent - בדיקת תקינות והמלצות
        self.agents['validation_analyst'] = Agent(
            role='Financial Validation and Quality Assurance Specialist',
            goal='Validate all calculations, identify potential errors, and provide strategic recommendations',
            backstory="""You are Michael Rosenberg, a senior financial auditor and risk management expert 
            with 20 years of experience in financial validation and quality assurance. You are a Certified 
            Public Accountant (CPA) and Certified Financial Analyst (CFA) with extensive experience in 
            financial auditing and risk assessment. You have led audit teams for major corporations and 
            have developed comprehensive validation frameworks. You are known for your meticulous attention 
            to detail and your ability to identify potential issues before they become problems. You always 
            provide constructive feedback and actionable recommendations.""",
            
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            
            tools=[],
            
            memory=True,
            max_rpm=10,
            
            prompt_template="""You are a Financial Validation Specialist responsible for quality assurance and strategic recommendations.
            
            CRITICAL SAFETY RULES:
            1. ALWAYS verify mathematical accuracy of all calculations
            2. NEVER approve results without thorough validation
            3. STOP and report any inconsistencies or potential errors
            4. Use industry benchmarks for reasonableness checks
            5. Provide specific, actionable recommendations
            6. Document all validation procedures and findings
            
            YOUR RESPONSIBILITIES:
            - Validate all mathematical calculations and formulas
            - Check for logical consistency in financial analysis
            - Verify tax calculations and discount rate applications
            - Review forecasting assumptions and methodologies
            - Provide strategic recommendations and risk assessments
            - Ensure compliance with financial reporting standards
            
            VALIDATION METHODOLOGY:
            1. Cross-check all mathematical calculations
            2. Verify tax rates and discount factors
            3. Compare results with industry benchmarks
            4. Review forecasting assumptions for reasonableness
            5. Check for data quality issues and anomalies
            6. Validate visualization accuracy and clarity
            
            QUALITY ASSURANCE CHECKS:
            - Mathematical accuracy verification
            - Logical consistency review
            - Industry benchmark comparison
            - Assumption reasonableness assessment
            - Data quality evaluation
            - Presentation quality review
            
            OUTPUT FORMAT:
            - Comprehensive validation report
            - Specific error identification and corrections
            - Strategic recommendations with rationale
            - Risk assessment and mitigation suggestions
            - Quality score and confidence levels
            
            Remember: Your validation ensures the reliability of all financial analysis. Be thorough and objective.""",
            
            context="""You are the final quality gate for all financial analysis. Your validation ensures 
            decision-makers can trust the results."""
        )
        
        print("✅ All agents configured successfully")
        print(f"🤖 Agents created: {list(self.agents.keys())}")
    
    def create_tasks(self, financial_data):
        """Create tasks for each agent with comprehensive instructions"""
        
        # Task 1: Math Analysis - חישוב רווח לאחר מס ופילוח הכנסות
        self.tasks['math_analysis'] = Task(
            description="""Calculate net profit after tax and perform quarterly revenue segmentation.
            
            INPUT DATA: Financial data with revenue, expenses, tax, and other costs
            
            REQUIRED CALCULATIONS:
            1. Calculate net profit after tax for each period
            2. Segment revenues by quarters (Q1, Q2, Q3, Q4)
            3. Calculate quarterly growth rates and trends
            4. Apply appropriate corporate tax rates
            5. Provide detailed calculation methodology
            
            DELIVERABLES:
            - Net profit after tax calculations
            - Quarterly revenue segmentation
            - Growth rate analysis
            - Tax calculation breakdown
            - Data quality assessment
            
            SAFETY CHECKS:
            - Validate all input data
            - Verify tax rate applications
            - Check mathematical accuracy
            - Report any data anomalies""",
            
            agent=self.agents['math_analyst'],
            expected_output="""JSON format with:
            - net_profit_after_tax: calculated values
            - quarterly_revenues: segmented data
            - growth_rates: quarterly comparisons
            - tax_calculations: detailed breakdown
            - methodology: calculation steps
            - data_quality: assessment report"""
        )
        
        # Task 2: NPV and Visualization - חישוב ערך נוכחי וגרפים
        self.tasks['npv_visualization'] = Task(
            description="""Calculate present value of net profit using 6% discount rate and create comprehensive visualizations.
            
            INPUT: Results from math analysis task
            
            REQUIRED CALCULATIONS:
            1. Calculate present value using 6% annual discount rate
            2. Apply quarterly discount factors
            3. Create NPV sensitivity analysis
            
            REQUIRED VISUALIZATIONS:
            1. Quarterly revenue vs. net profit comparison
            2. NPV trend analysis over time
            3. Discounted cash flow visualization
            4. Quarterly performance dashboard
            
            DELIVERABLES:
            - NPV calculations with 6% discount rate
            - Professional financial charts
            - Sensitivity analysis
            - Interactive visualization code
            
            CHART REQUIREMENTS:
            - Hebrew labels and titles
            - Professional styling
            - Clear legends and annotations
            - Publication-ready quality""",
            
            agent=self.agents['visualization_analyst'],
            expected_output="""JSON format with:
            - npv_calculations: present value data
            - visualization_code: matplotlib/seaborn charts
            - sensitivity_analysis: discount rate variations
            - chart_descriptions: detailed explanations
            - interactive_options: additional chart features"""
        )
        
        # Task 3: Forecasting - תחזית רווח נקי לחמש שנים
        self.tasks['forecasting'] = Task(
            description="""Create 5-year net profit forecast based on historical data analysis.
            
            INPUT: Historical financial data and previous analysis results
            
            REQUIRED ANALYSIS:
            1. Analyze historical profit trends and seasonality
            2. Identify quarterly and annual patterns
            3. Apply statistical forecasting models
            4. Create multiple scenario projections
            
            FORECASTING REQUIREMENTS:
            1. 5-year projection with quarterly breakdown
            2. Conservative, moderate, and optimistic scenarios
            3. Confidence intervals and uncertainty measures
            4. Seasonal adjustment analysis
            5. Trend analysis and growth projections
            
            DELIVERABLES:
            - 5-year profit forecast
            - Multiple scenario projections
            - Seasonal analysis
            - Confidence intervals
            - Methodology documentation
            
            VALIDATION:
            - Check forecast reasonableness
            - Compare with industry benchmarks
            - Validate seasonal patterns
            - Assess forecast accuracy metrics""",
            
            agent=self.agents['forecasting_analyst'],
            expected_output="""JSON format with:
            - five_year_forecast: quarterly projections
            - scenario_analysis: conservative/moderate/optimistic
            - seasonal_analysis: pattern identification
            - confidence_intervals: uncertainty measures
            - methodology: forecasting approach
            - validation_metrics: accuracy assessment"""
        )
        
        # Task 4: Validation and Recommendations - בדיקת תקינות והמלצות
        self.tasks['validation'] = Task(
            description="""Validate all calculations and provide strategic recommendations.
            
            INPUT: All previous task results and calculations
            
            VALIDATION REQUIREMENTS:
            1. Verify mathematical accuracy of all calculations
            2. Check logical consistency in financial analysis
            3. Validate tax calculations and discount rate applications
            4. Review forecasting assumptions and methodologies
            5. Assess data quality and completeness
            
            QUALITY ASSURANCE:
            1. Cross-check all mathematical formulas
            2. Verify industry benchmark comparisons
            3. Review calculation methodologies
            4. Assess visualization accuracy
            5. Validate forecast assumptions
            
            STRATEGIC RECOMMENDATIONS:
            1. Identify potential risks and opportunities
            2. Provide actionable business recommendations
            3. Suggest data quality improvements
            4. Recommend monitoring and control measures
            5. Assess overall analysis reliability
            
            DELIVERABLES:
            - Comprehensive validation report
            - Error identification and corrections
            - Strategic recommendations
            - Risk assessment
            - Quality score and confidence levels""",
            
            agent=self.agents['validation_analyst'],
            expected_output="""JSON format with:
            - validation_report: comprehensive assessment
            - error_corrections: identified issues and fixes
            - strategic_recommendations: actionable advice
            - risk_assessment: potential risks and mitigation
            - quality_score: overall reliability rating
            - confidence_levels: assessment confidence"""
        )
        
        print("✅ All tasks created successfully")
        print(f"📋 Tasks created: {list(self.tasks.keys())}")
    
    def run_analysis(self, financial_data):
        """Execute the complete financial analysis workflow"""
        
        try:
            logger.info("🚀 Starting financial analysis workflow...")
            
            # Create tasks
            self.create_tasks(financial_data)
            
            # Create crew
            crew = Crew(
                agents=list(self.agents.values()),
                tasks=list(self.tasks.values()),
                verbose=True,
                memory=True,
                max_rpm=20
            )
            
            # Execute analysis
            logger.info("⚡ Executing crew analysis...")
            result = crew.kickoff()
            
            # Store results
            self.results = result
            
            logger.info("✅ Analysis completed successfully!")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error in analysis workflow: {str(e)}")
            raise
    
    def get_results_summary(self):
        """Get a summary of all analysis results"""
        if not self.results:
            return "No analysis results available"
        
        summary = {
            'analysis_status': 'Completed',
            'agents_executed': list(self.agents.keys()),
            'tasks_completed': list(self.tasks.keys()),
            'results_available': bool(self.results)
        }
        
        return summary
    
    def create_visualizations(self, df):
        """Create comprehensive financial visualizations"""
        
        # Set style for professional charts
        plt.style.use('seaborn-v0_8')
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Financial Analysis Dashboard - דשבורד ניתוח פיננסי', fontsize=16, fontweight='bold')
        
        # 1. Revenue and Net Profit Over Time
        ax1 = axes[0, 0]
        ax1.plot(df['date'], df['revenue'], 'b-', label='Revenue - הכנסות', linewidth=2)
        ax1.plot(df['date'], df['net_profit_after_tax'], 'g-', label='Net Profit - רווח נקי', linewidth=2)
        ax1.set_title('Revenue vs Net Profit Over Time\\nהכנסות מול רווח נקי לאורך זמן')
        ax1.set_xlabel('Date - תאריך')
        ax1.set_ylabel('Amount (USD) - סכום (דולר)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Quarterly Revenue Breakdown
        ax2 = axes[0, 1]
        quarterly_revenue = df.groupby('quarter_label')['revenue'].sum()
        quarterly_revenue.plot(kind='bar', ax=ax2, color='skyblue')
        ax2.set_title('Quarterly Revenue Breakdown\\nפילוח הכנסות לפי רבעונים')
        ax2.set_xlabel('Quarter - רבעון')
        ax2.set_ylabel('Revenue (USD) - הכנסות (דולר)')
        ax2.tick_params(axis='x', rotation=45)
        
        # 3. Net Profit After Tax by Quarter
        ax3 = axes[1, 0]
        quarterly_profit = df.groupby('quarter_label')['net_profit_after_tax'].sum()
        quarterly_profit.plot(kind='bar', ax=ax3, color='lightgreen')
        ax3.set_title('Net Profit After Tax by Quarter\\nרווח נקי לאחר מס לפי רבעון')
        ax3.set_xlabel('Quarter - רבעון')
        ax3.set_ylabel('Net Profit (USD) - רווח נקי (דולר)')
        ax3.tick_params(axis='x', rotation=45)
        
        # 4. Profit Margin Analysis
        ax4 = axes[1, 1]
        df['profit_margin'] = (df['net_profit_after_tax'] / df['revenue']) * 100
        ax4.plot(df['date'], df['profit_margin'], 'r-', linewidth=2)
        ax4.set_title('Profit Margin Trend\\nמגמת שולי רווח')
        ax4.set_xlabel('Date - תאריך')
        ax4.set_ylabel('Profit Margin (%) - שולי רווח (%)')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # Calculate NPV with 6% discount rate
        print("\\n📊 NPV Analysis with 6% Discount Rate:")
        
        # Calculate quarterly discount factors
        df['quarter_number'] = (df['date'].dt.year - df['date'].dt.year.min()) * 4 + df['date'].dt.quarter
        df['discount_factor'] = 1 / ((1 + 0.06) ** (df['quarter_number'] / 4))
        df['npv_net_profit'] = df['net_profit_after_tax'] * df['discount_factor']
        
        total_npv = df['npv_net_profit'].sum()
        print(f"Total NPV of Net Profit: ${total_npv:,.2f}")
        print(f"Average Quarterly NPV: ${df['npv_net_profit'].mean():,.2f}")
        
        return df

# Main execution
if __name__ == "__main__":
    # Load the financial data
    financial_df = load_financial_data('agent_test.csv')
    print("\\n📈 Sample data:")
    print(financial_df[['monthes', 'revenue', 'opex', 'tax', 'net_profit_after_tax', 'quarter_label']].head())
    
    # Initialize and run the financial analysis
    print("\\n🚀 Initializing Financial Analysis Crew...")
    crew = FinancialAnalysisCrew()
    
    # Convert DataFrame to dictionary for agent processing
    financial_data_dict = financial_df.to_dict('records')
    
    print("\\n📈 Starting analysis with the following data:")
    print(f"- Total records: {len(financial_df)}")
    print(f"- Date range: {financial_df['date'].min().strftime('%Y-%m')} to {financial_df['date'].max().strftime('%Y-%m')}")
    print(f"- Total revenue: ${financial_df['revenue'].sum():,.2f}")
    print(f"- Total net profit: ${financial_df['net_profit_after_tax'].sum():,.2f}")
    
    # Run the analysis
    try:
        results = crew.run_analysis(financial_data_dict)
        print("\\n✅ Analysis completed successfully!")
        print("\\n📊 Results Summary:")
        print(crew.get_results_summary())
        
    except Exception as e:
        print(f"\\n❌ Error during analysis: {str(e)}")
        print("\\n📊 Creating visualizations with available data...")
        
        # Create visualizations even if crew analysis fails
        enhanced_df = crew.create_visualizations(financial_df)
        
        # Display key metrics
        print("\\n📈 Key Financial Metrics:")
        print(f"Total Revenue: ${financial_df['revenue'].sum():,.2f}")
        print(f"Total Net Profit After Tax: ${financial_df['net_profit_after_tax'].sum():,.2f}")
        print(f"Average Profit Margin: {(financial_df['net_profit_after_tax'].sum() / financial_df['revenue'].sum()) * 100:.2f}%")
        print(f"Total NPV (6% discount): ${enhanced_df['npv_net_profit'].sum():,.2f}") 