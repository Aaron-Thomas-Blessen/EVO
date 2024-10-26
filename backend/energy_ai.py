import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta

class EnergyAIOptimizer:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100)
        self.scaler = StandardScaler()
        self.feature_columns = None  # Store feature columns after training
        
    def prepare_features(self, df):
        """Convert timestamp to useful features"""
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        
        # One-hot encode categorical features
        hour_encoded = pd.get_dummies(df['hour'], prefix='hour')
        day_encoded = pd.get_dummies(df['day_of_week'], prefix='day')
        
        # Combine features
        features = pd.concat([
            hour_encoded,
            day_encoded,
            df[['is_weekend']],
        ], axis=1)
        
        # If this is prediction time and we have stored feature columns
        if self.feature_columns is not None:
            # Add missing columns with zeros
            for col in self.feature_columns:
                if col not in features.columns:
                    features[col] = 0
            # Ensure columns are in the same order as during training
            features = features[self.feature_columns]
        
        return features

    def generate_sample_data(self, days=7):
        """Generate realistic sample data for demonstration"""
        start_date = datetime.now() - timedelta(days=days)
        dates = pd.date_range(start_date, periods=days*24, freq='H')
        
        # Create base usage pattern
        base_usage = np.sin(np.linspace(0, 2*np.pi*days, days*24)) * 2 + 5
        
        # Add daily patterns
        hour_pattern = np.tile(np.sin(np.linspace(0, 2*np.pi, 24)) * 1.5, days)
        
        # Add random noise
        noise = np.random.normal(0, 0.5, days*24)
        
        # Combine patterns
        usage = base_usage + hour_pattern + noise
        
        # Ensure non-negative values
        usage = np.maximum(usage, 0)
        
        return pd.DataFrame({
            'timestamp': dates,
            'usage': usage
        })

    def train(self, data=None):
        """Train the model on historical energy usage data"""
        if data is None:
            data = self.generate_sample_data()
            
        # Prepare features and target
        X = self.prepare_features(data)
        # Store feature columns for prediction
        self.feature_columns = X.columns.tolist()
        y = data['usage']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        # Train model
        self.model.fit(X_train, y_train)
        return self.model.score(X_test, y_test)

    def predict_usage(self, future_dates):
        """Predict future energy usage"""
        future_df = pd.DataFrame({'timestamp': future_dates})
        features = self.prepare_features(future_df)
        predictions = self.model.predict(features)
        return predictions

    def get_optimization_recommendations(self, current_usage, predicted_usage):
        """Generate optimization recommendations based on predictions"""
        recommendations = []
        
        # Check for unusual spikes
        if current_usage > predicted_usage * 1.2:
            recommendations.append({
                'type': 'alert',
                'message': 'Unusual energy spike detected',
                'potential_savings': f'{(current_usage - predicted_usage) * 0.15:.2f}$'
            })

        # Time-of-use optimization
        peak_hours = list(range(17, 21))  # 5 PM to 8 PM
        current_hour = datetime.now().hour
        
        if current_hour in peak_hours:
            recommendations.append({
                'type': 'shift',
                'message': 'Currently in peak hours. Consider shifting heavy appliance usage to off-peak hours',
                'potential_savings': '0.45$ per kWh'
            })

        return recommendations

    def get_real_time_insights(self, current_data):
        """Generate real-time insights from current usage patterns"""
        # Predict expected usage
        features = self.prepare_features(pd.DataFrame({'timestamp': [current_data['timestamp']]}))
        expected_usage = self.model.predict(features)[0]
        
        # Calculate efficiency score
        efficiency_score = 100 - min(100, max(0, 
            ((current_data['usage'] - expected_usage) / expected_usage) * 100))
        
        return {
            'current_usage': current_data['usage'],
            'expected_usage': expected_usage,
            'efficiency_score': int(efficiency_score),
            'recommendations': self.get_optimization_recommendations(
                current_data['usage'], 
                expected_usage
            )
        }