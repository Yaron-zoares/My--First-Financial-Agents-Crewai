# Financial Analysis CrewAI System
# מערכת ניתוח פיננסי CrewAI

## 📊 Project Overview

This project implements a comprehensive financial analysis system using CrewAI framework with four specialized AI agents. The system performs detailed financial calculations, generates visualizations, and provides forecasting capabilities based on CSV financial data.

## 🎯 Features

### 🤖 AI Agents
- **Financial Math Analyst**: Handles complex calculations and quarterly revenue segmentation
- **Financial Visualization & NPV Analyst**: Creates charts and calculates Net Present Value
- **Financial Forecasting Specialist**: Performs 5-year profit forecasting with trend analysis
- **Financial Validation Specialist**: Validates results and provides recommendations

### 📈 Analysis Capabilities
- **Net Profit After Tax Calculations**
- **Quarterly Revenue Segmentation**
- **NPV Analysis (6% discount rate)**
- **5-Year Financial Forecasting**
- **Cost Structure Analysis**
- **Growth Rate Calculations**
- **Statistical Analysis**
- **Professional Visualizations**

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Basic Usage
```bash
# Run the main financial analysis
python financial_analysis_crew.py

# Display detailed results
python detailed_results.py

# Generate visualizations
python create_visualizations.py
```

## 📁 Project Structure

```
CREWAI/
├── financial_analysis_crew.py    # Main CrewAI system
├── detailed_results.py           # Detailed results display
├── create_visualizations.py      # Visualization generation
├── financial_report.md          # Comprehensive report
├── agent_test.csv              # Sample financial data
├── requirements.txt             # Python dependencies
└── README.md                   # This file
```

## 📊 Sample Output

### Key Metrics
- **Total Revenue**: $2,655,527.00
- **Total Net Profit**: $1,625,475.17
- **NPV (6% discount)**: $1,469,104.35
- **Average Profit Margin**: 58.79%

### Quarterly Analysis
| Quarter | Revenue | Net Profit | NPV |
|---------|---------|------------|-----|
| Q1-2026 | $977,783 | $658,924 | $612,636 |
| Q2-2027 | $977,783 | $542,670 | $469,106 |
| Q4-2025 | $274,555 | $184,245 | $173,816 |

## 🔧 Configuration

### Environment Variables
The system uses environment variables for API configuration:
- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL_NAME`: Model name (default: gpt-3.5-turbo)

### Data Format
The system expects CSV files with the following columns:
- `monthes`: Date in format "Jan-25"
- `revenue`: Revenue amount
- `opex`: Operating expenses
- `tax`: Tax amount
- `fianance cost`: Finance costs
- `sg@a`: SG&A expenses

## 📈 Analysis Features

### 1. Financial Calculations
- Net profit after tax calculation
- Profit margin analysis
- NPV calculations with 6% discount rate
- Quarterly aggregation

### 2. Visualization
- Revenue vs. Net Profit charts
- Quarterly breakdown visualizations
- NPV analysis graphs
- Cost structure pie charts
- Growth rate analysis

### 3. Forecasting
- 5-year revenue projections
- Conservative, moderate, and optimistic scenarios
- Trend-based forecasting
- Seasonal pattern analysis

### 4. Statistical Analysis
- Descriptive statistics
- Growth rate calculations
- Performance metrics
- Cost structure analysis

## 🛠️ Technical Details

### Dependencies
- **CrewAI**: AI agent orchestration framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Matplotlib**: Data visualization
- **Seaborn**: Statistical data visualization
- **Python-dotenv**: Environment variable management

### Architecture
The system follows a modular architecture:
1. **Data Loading**: CSV processing and validation
2. **Agent Setup**: Four specialized AI agents
3. **Task Execution**: Parallel task processing
4. **Analysis**: Comprehensive financial calculations
5. **Visualization**: Professional chart generation
6. **Reporting**: Detailed markdown reports

## 📋 Usage Examples

### Basic Analysis
```python
from financial_analysis_crew import FinancialAnalysisCrew

# Load data
crew = FinancialAnalysisCrew()
financial_data = crew.load_financial_data('agent_test.csv')

# Run analysis
results = crew.run_analysis(financial_data)
```

### Detailed Results
```python
from detailed_results import load_and_analyze_data, display_detailed_results

# Load and analyze
df = load_and_analyze_data('agent_test.csv')
display_detailed_results(df)
```

## 🎨 Visualization Features

The system generates professional financial charts:
- **Revenue vs. Net Profit Over Time**
- **Profit Margin Trend Analysis**
- **Quarterly Revenue Breakdown**
- **NPV Analysis Charts**
- **Monthly Revenue Heatmap**
- **Cost Structure Pie Chart**
- **Growth Rate Analysis**

## 📊 Sample Results

### Performance Highlights
- **Best Revenue Month**: March 2026 ($800,003)
- **Best Profit Month**: March 2026 ($539,642)
- **Growth Rate**: 163.33% overall growth
- **NPV Retention**: 90.4% of profits

### Forecast Scenarios
- **Conservative**: $32,679 revenue, $16,907 profit
- **Moderate**: $46,347 revenue, $22,402 profit
- **Optimistic**: $65,339 revenue, $29,566 profit

## 🔍 Quality Assurance

### Data Validation
- CSV format validation
- Missing data handling
- Outlier detection
- Data consistency checks

### Calculation Verification
- Mathematical accuracy verification
- Cross-validation with industry benchmarks
- Statistical significance testing
- Error handling and logging

## 📝 Reports Generated

1. **Comprehensive Financial Report** (`financial_report.md`)
   - Executive summary
   - Key metrics
   - Quarterly analysis
   - Strategic insights
   - Methodology documentation

2. **Detailed Results Output**
   - Monthly breakdown
   - Statistical summaries
   - Performance highlights
   - Forecast analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- CrewAI framework for AI agent orchestration
- OpenAI for language model capabilities
- Financial analysis community for best practices

## 📞 Support

For questions or issues:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information

---

**Note**: This system is designed for educational and analytical purposes. Always verify financial calculations independently for critical business decisions. 