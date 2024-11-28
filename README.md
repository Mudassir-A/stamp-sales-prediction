
# Time Series-Stamp Sales: 
### Indian Postal Revenue Prediction

A comprehensive time series analysis and prediction system for sales data, with a focus on Indian stamp sales. The project includes data generation, multiple prediction methods, and detailed visualizations.

## Features

- Data generation with realistic patterns including:
  - Seasonal variations
  - Holiday effects (Indian holidays)
  - Weekday/weekend patterns
  - Long-term trends
- Multiple prediction methods:
  - Simple Exponential Smoothing
  - Holt-Winters Exponential Smoothing
  - ARIMA Forecasting
- Comprehensive visualizations:
  - Overall sales predictions
  - Yearly patterns
  - Monthly patterns
  - Future predictions
- CSV exports for further analysis

## Installation

```bash
# Clone the repository
git clone https://github.com/Mudassir-A/stamp-sales-prediction.git
cd stamp-sales-prediction

# Install required packages
pip install -r requirements.txt
```

## Usage

1. First, generate the sample dataset:
```bash
python data_builder.py
```
This will create `stamp_sales_data.csv` with synthetic sales data from 2010 to 2024.

2. Run the prediction model:
```bash
python model.py
```
This will:
- Load the generated data
- Perform predictions using multiple methods
- Generate visualizations in the `output_predictions` directory
- Save prediction results as CSVs in `output_predictions/csv`

## Output Structure

```
output_predictions/
├── csv/
│   ├── historical_data.csv
│   ├── monthly_predictions.csv
│   ├── overall_predictions.csv
│   └── yearly_predictions.csv
├── comprehensive_sales_predictions.png
├── month_*_sales_prediction.png
├── overall_sales_prediction.png
└── year_*_sales_prediction.png
```

## Files Description

- `data_builder.py`: Generates synthetic sales data with realistic patterns
- `model.py`: Contains the main prediction logic and visualization code
- `output_predictions/`: Directory containing all generated predictions and visualizations

## Prediction Methods

1. **Simple Exponential Smoothing**: Best for data with no clear trend or seasonality
2. **Holt-Winters**: Handles both trend and seasonal patterns
3. **ARIMA**: Captures complex time series patterns

<!-- ## Contributing

Feel free to submit issues and enhancement requests! -->

## License

[MIT License](https://github.com/Mudassir-A/stamp-sales-prediction/blob/master/model.py)
