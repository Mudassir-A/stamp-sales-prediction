# 📈 Time Series-Stamp Sales: 
### 🏤 Indian Postal Revenue Prediction

A comprehensive time series analysis and prediction system for sales data, with a focus on Indian stamp sales. The project includes data generation, multiple prediction methods, and detailed visualizations.

## ✨ Features

- 📊 Data generation with realistic patterns including:
  - 🌊 Seasonal variations
  - 🎉 Holiday effects (Indian holidays)
  - 📅 Weekday/weekend patterns
  - 📈 Long-term trends
- 🔮 Multiple prediction methods:
  - 📊 Simple Exponential Smoothing
  - 📈 Holt-Winters Exponential Smoothing
  - 📉 ARIMA Forecasting
- 📊 Comprehensive visualizations:
  - 🎯 Overall sales predictions
  - 📆 Yearly patterns
  - 📅 Monthly patterns
  - 🔮 Future predictions
- 📁 CSV exports for further analysis
- 🔍 Stamp Vision: AI-powered stamp analysis using Google's Gemini model
  - 🏷️ Stamp identification
  - 📚 Historical and cultural information
  - 💰 Price and issue date detection
  - ✅ Visual authentication

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/Mudassir-A/stamp-sales-prediction.git
cd stamp-sales-prediction

# Install required packages
pip install -r requirements.txt

# Create a .env file and add your Google API key
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

### 🔑 Setting up the Environment File

1. Create a `.env` file in the root directory of the project
2. Get your Google API key from the [Google AI Studio](https://makersuite.google.com/app/apikey)
3. Add your API key to the `.env` file in this format:
```plaintext
GOOGLE_API_KEY=your_actual_api_key_here
```

⚠️ **Important**: 
- Never commit your `.env` file to version control
- Keep your API key secure and don't share it publicly
- The `.env` file is already included in `.gitignore`

## 🎮 Usage

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

3. Run the Stamp Vision analyzer:
```bash
streamlit run stamp_vision.py
```
This will:
- Launch a web interface for stamp analysis
- Allow you to upload stamp images
- Provide detailed information about uploaded stamps including name, date of issue, price, and historical significance

## 📁 Output Structure

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

## 📝 Files Description

- 📊 `data_builder.py`: Generates synthetic sales data with realistic patterns
- 🤖 `model.py`: Contains the main prediction logic and visualization code
- 📂 `output_predictions/`: Directory containing all generated predictions and visualizations
- 🔍 `stamp_vision.py`: AI-powered stamp analyzer using Google's Gemini model for visual stamp identification and analysis

## 🎯 Prediction Methods

1. 📊 **Simple Exponential Smoothing**: Best for data with no clear trend or seasonality
2. 📈 **Holt-Winters**: Handles both trend and seasonal patterns
3. 📉 **ARIMA**: Captures complex time series patterns

<!-- ## Contributing

Feel free to submit issues and enhancement requests! -->

## 📄 License

[MIT License](https://github.com/Mudassir-A/stamp-sales-prediction/blob/master/model.py)
