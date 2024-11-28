import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
import warnings


class TimeSeriesSalesPrediction:
    def __init__(self, data_path):
        """
        Initialize time series sales prediction

        :param data_path: Path to the CSV file containing sales data
        """
        # Suppress warnings
        warnings.filterwarnings("ignore")

        # Create output directories
        import os

        os.makedirs("output_predictions", exist_ok=True)
        os.makedirs("output_predictions/csv", exist_ok=True)

        # Load data
        self.df = pd.read_csv(data_path)
        self.df["Date"] = pd.to_datetime(self.df["Date"])
        self.df.set_index("Date", inplace=True)

        # Prepare time series data
        self.prepare_time_series()

    def prepare_time_series(self):
        """
        Prepare time series data for prediction
        """
        # Resample data to different granularities
        self.daily_sales = self.df["Sales"]
        self.weekly_sales = self.daily_sales.resample("W").mean()
        self.monthly_sales = self.daily_sales.resample("M").mean()
        self.yearly_sales = self.daily_sales.resample("Y").mean()

    def predict_time_series(self, series, pred_periods=12, granularity="Sales"):
        """
        Perform time series prediction using multiple methods

        :param series: Time series data
        :param pred_periods: Number of periods to predict
        :param granularity: Granularity of the prediction (for naming)
        :return: Prediction results and visualization
        """
        # Prepare data
        data = series.dropna()

        # Split data into train and test
        train_size = int(len(data) * 0.8)
        train, test = data[:train_size], data[train_size:]

        # Prediction methods
        prediction_results = {}

        # 1. Simple Exponential Smoothing
        model_ses = ExponentialSmoothing(train, trend=None, seasonal=None).fit()
        ses_forecast = model_ses.forecast(steps=pred_periods)
        prediction_results["Simple Exponential Smoothing"] = ses_forecast

        # 2. Holt-Winters Exponential Smoothing (Seasonal)
        try:
            model_hw = ExponentialSmoothing(
                train, trend="add", seasonal="add", seasonal_periods=len(train) // 4
            ).fit()
            hw_forecast = model_hw.forecast(steps=pred_periods)
            prediction_results["Holt-Winters"] = hw_forecast
        except:
            pass

        # 3. ARIMA Forecasting
        try:
            model_arima = ARIMA(train, order=(5, 1, 0)).fit()
            arima_forecast = model_arima.forecast(steps=pred_periods)
            prediction_results["ARIMA"] = arima_forecast
        except:
            pass

        # Visualization
        plt.figure(figsize=(15, 8))

        # Original data
        plt.plot(data.index, data.values, label="Historical Data", color="blue")

        # Test data
        plt.plot(test.index, test.values, label="Test Data", color="green")

        # Predictions
        pred_index = pd.date_range(
            start=data.index[-1], periods=pred_periods + 1, freq=data.index.freq or "D"
        )[1:]

        for method, forecast in prediction_results.items():
            plt.plot(pred_index, forecast, label=f"{method} Prediction", linestyle="--")

        plt.title(f"{granularity} Time Series Prediction")
        plt.xlabel("Date")
        plt.ylabel("Sales")
        plt.legend()
        plt.tight_layout()
        plt.savefig(
            f'output_predictions/{granularity.lower().replace(" ", "_")}_prediction.png'
        )
        plt.close()

        # Calculate prediction accuracy
        print(f"\n{granularity} Prediction Accuracy:")
        for method, forecast in prediction_results.items():
            if len(forecast) <= len(test):
                mse = mean_squared_error(test[: len(forecast)], forecast)
                mae = mean_absolute_error(test[: len(forecast)], forecast)
                print(f"{method}:")
                print(f"  Mean Squared Error: {mse:.2f}")
                print(f"  Mean Absolute Error: {mae:.2f}")

        return prediction_results

    def comprehensive_prediction(self):
        """
        Perform predictions at different granularities
        """
        # Overall dataset prediction
        overall_prediction = self.predict_time_series(
            self.daily_sales, pred_periods=365, granularity="Overall Sales"
        )

        # Yearly predictions for each year
        yearly_predictions = {}
        for year in self.daily_sales.index.year.unique():
            year_data = self.daily_sales[self.daily_sales.index.year == year]
            yearly_predictions[year] = self.predict_time_series(
                year_data, pred_periods=52, granularity=f"Year {year} Sales"
            )

        # Prediction for each future year
        future_yearly_predictions = {}
        for year in range(
            self.daily_sales.index.year.max() + 1, self.daily_sales.index.year.max() + 4
        ):
            future_yearly_predictions[year] = self.predict_time_series(
                self.daily_sales[self.daily_sales.index.year < year],
                pred_periods=365,
                granularity=f"Future Year {year} Sales",
            )

        # Monthly predictions for each month
        monthly_predictions = {}
        for month in range(1, 13):
            month_data = self.daily_sales[self.daily_sales.index.month == month]
            monthly_predictions[month] = self.predict_time_series(
                month_data, pred_periods=30, granularity=f"Month {month} Sales"
            )

        # Prediction for each future month
        future_monthly_predictions = {}
        current_year = self.daily_sales.index.year.max()
        for month in range(1, 13):
            future_monthly_predictions[month] = self.predict_time_series(
                self.daily_sales[
                    (self.daily_sales.index.year < current_year)
                    & (self.daily_sales.index.month == month)
                ],
                pred_periods=30,
                granularity=f"Future Month {month} Sales",
            )

        return {
            "overall": overall_prediction,
            "yearly": yearly_predictions,
            "future_yearly": future_yearly_predictions,
            "monthly": monthly_predictions,
            "future_monthly": future_monthly_predictions,
        }

    def visualize_predictions(self, predictions):
        """
        Create comprehensive visualizations of predictions
        """
        # Prepare figure with multiple subplots
        plt.figure(figsize=(20, 15))

        # 1. Overall Sales Prediction
        plt.subplot(2, 2, 1)
        overall_data = self.daily_sales
        plt.plot(
            overall_data.index,
            overall_data.values,
            label="Historical Data",
            color="blue",
        )

        # Overlay future predictions from first prediction method
        first_method = list(predictions["overall"].keys())[0]
        future_index = pd.date_range(
            start=overall_data.index[-1],
            periods=len(predictions["overall"][first_method]) + 1,
            freq="D",
        )[1:]
        plt.plot(
            future_index,
            predictions["overall"][first_method],
            label="Future Sales Prediction",
            color="red",
            linestyle="--",
        )
        plt.title("Overall Sales Prediction")
        plt.xlabel("Date")
        plt.ylabel("Sales")
        plt.legend()

        # 2. Yearly Sales Prediction
        plt.subplot(2, 2, 2)
        yearly_avg = self.daily_sales.resample("Y").mean()
        plt.plot(
            yearly_avg.index,
            yearly_avg.values,
            label="Historical Yearly Average",
            marker="o",
        )

        # Future yearly predictions - Modified code
        future_years = list(predictions["future_yearly"].keys())
        future_year_preds = []
        for year in future_years:
            pred_dict = predictions["future_yearly"][year]
            first_method = list(pred_dict.keys())[0]  # Get first prediction method
            pred_values = pred_dict[first_method]
            future_year_preds.append(pred_values.mean())  # Use mean of predictions

        future_year_index = [pd.to_datetime(f"{year}-01-01") for year in future_years]
        plt.plot(
            future_year_index,
            future_year_preds,
            label="Future Yearly Predictions",
            color="green",
            marker="s",
        )
        plt.title("Yearly Sales Prediction")
        plt.xlabel("Year")
        plt.ylabel("Average Sales")
        plt.legend()

        # 3. Monthly Sales Pattern
        plt.subplot(2, 2, 3)
        monthly_avg = self.daily_sales.groupby(self.daily_sales.index.month).mean()
        plt.bar(monthly_avg.index, monthly_avg.values)
        plt.title("Average Sales by Month")
        plt.xlabel("Month")
        plt.ylabel("Average Sales")

        # 4. Future Monthly Predictions - Modified code
        plt.subplot(2, 2, 4)
        future_month_preds = []
        for month in range(1, 13):
            pred_dict = predictions["future_monthly"][month]
            first_method = list(pred_dict.keys())[0]
            pred_values = pred_dict[first_method]
            future_month_preds.append(pred_values.mean())  # Use mean of predictions

        plt.bar(range(1, 13), future_month_preds)
        plt.title("Predicted Sales for Each Month")
        plt.xlabel("Month")
        plt.ylabel("Predicted Sales")

        plt.tight_layout()
        plt.savefig("output_predictions/comprehensive_sales_predictions.png")
        plt.close()

    def save_predictions_to_csv(self, predictions):
        """
        Save prediction results to CSV files for web visualization
        """
        # Save overall predictions
        overall_df = pd.DataFrame()
        # Get the length of predictions from the first method's forecast
        first_method = list(predictions['overall'].keys())[0]
        pred_length = len(predictions['overall'][first_method])
        
        pred_index = pd.date_range(
            start=self.daily_sales.index[-1],
            periods=pred_length + 1,
            freq='D'
        )[1:]
        
        for method, forecast in predictions['overall'].items():
            overall_df[f'{method}'] = forecast
        overall_df.index = pred_index
        overall_df.to_csv('output_predictions/csv/overall_predictions.csv')

        # Save yearly predictions
        yearly_df = pd.DataFrame()
        for year, pred_dict in predictions['future_yearly'].items():
            for method, forecast in pred_dict.items():
                yearly_df[f'{year}_{method}'] = forecast
        yearly_df.to_csv('output_predictions/csv/yearly_predictions.csv')

        # Save monthly predictions
        monthly_df = pd.DataFrame()
        for month, pred_dict in predictions['future_monthly'].items():
            for method, forecast in pred_dict.items():
                monthly_df[f'Month_{month}_{method}'] = forecast
        monthly_df.to_csv('output_predictions/csv/monthly_predictions.csv')

        # Save historical data for context
        historical_df = pd.DataFrame({
            'historical_sales': self.daily_sales,
            'weekly_avg': self.weekly_sales.reindex(self.daily_sales.index, method='ffill'),
            'monthly_avg': self.monthly_sales.reindex(self.daily_sales.index, method='ffill'),
            'yearly_avg': self.yearly_sales.reindex(self.daily_sales.index, method='ffill')
        })
        historical_df.to_csv('output_predictions/csv/historical_data.csv')


# Main execution
def main():
    # Assuming you have the previously generated stamp_sales_data.csv
    predictor = TimeSeriesSalesPrediction("stamp_sales_data.csv")
    predictions = predictor.comprehensive_prediction()
    predictor.visualize_predictions(predictions)
    predictor.save_predictions_to_csv(predictions)


if __name__ == "__main__":
    main()
