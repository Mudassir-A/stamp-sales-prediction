import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import holidays

def generate_stamp_sales_dataset():
    # Set random seed for reproducibility
    np.random.seed(42)

    # Generate date range
    start_date = datetime(2010, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')

    # Initialize dataset
    df = pd.DataFrame({'Date': date_range})

    # Add day of week
    df['Day_of_Week'] = df['Date'].dt.day_name()

    # Create Indian holiday list
    indian_holidays = holidays.IN(years=range(2010, 2025))

    # Holiday indicator
    df['Holiday_Indicator'] = df['Date'].apply(lambda x: 1 if x in indian_holidays else 0)

    # Base sales generation with seasonal and trend components
    def generate_sales(date):
        # Baseline trend: gradual increase over years
        base_trend = 300 + (date.year - 2010) * 10

        # Seasonal variation
        seasonal_factor = {
            'January': 1.2,   # Post-holiday season
            'February': 1.1,  # Tax season start
            'March': 1.3,     # Financial year end
            'April': 0.9,     # New financial year
            'May': 0.8,       # Pre-monsoon slowdown
            'June': 0.7,      # Monsoon
            'July': 0.9,      # Post-monsoon
            'August': 1.0,    # Independence Day spike
            'September': 1.1, # Post-independence period
            'October': 1.4,   # Festival season (Diwali)
            'November': 1.5,  # Peak festival season
            'December': 1.6   # End of year spike
        }[date.strftime('%B')]

        # Weekday vs weekend factor
        weekday_factor = 1.2 if date.weekday() < 5 else 0.7

        # Holiday spike
        holiday_factor = 1.5 if df.loc[df['Date'] == date, 'Holiday_Indicator'].values[0] == 1 else 1.0

        # Random noise
        noise = np.random.normal(1, 0.1)

        # Combine factors
        sales = base_trend * seasonal_factor * weekday_factor * holiday_factor * noise

        return max(100, min(1000, int(sales)))  # Constrain between 100-1000

    # Generate sales
    df['Sales'] = df['Date'].apply(generate_sales)

    # Save to CSV
    df.to_csv('stamp_sales_data.csv', index=False)
    
    return df

# Generate and display dataset
stamp_sales_data = generate_stamp_sales_dataset()
print(stamp_sales_data.head(10))
print("\nDataset Statistics:")
print(stamp_sales_data['Sales'].describe())

# Optional: Basic visualization
import matplotlib.pyplot as plt

plt.figure(figsize=(15, 6))
plt.plot(stamp_sales_data['Date'], stamp_sales_data['Sales'])
plt.title('Indian Stamp Sales Time Series')
plt.xlabel('Date')
plt.ylabel('Daily Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()