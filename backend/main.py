# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import pandas as pd
from energy_ai import EnergyAIOptimizer

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize our AI model
optimizer = EnergyAIOptimizer()
optimizer.train()  # Train with sample data

@app.get("/")
async def read_root():
    return {"status": "Energy Optimization API is running"}

@app.get("/api/current-status")
async def get_current_status():
    # Simulate current reading
    current_data = {
        'timestamp': datetime.now(),
        'usage': 6.5  # This would come from your smart meter
    }
    
    # Get AI insights
    insights = optimizer.get_real_time_insights(current_data)
    
    # Get predictions for next 24 hours
    future_dates = pd.date_range(datetime.now(), periods=24, freq='H')
    predictions = optimizer.predict_usage(future_dates)
    
    return {
        "current_status": insights,
        "predictions": [
            {
                "time": date.strftime("%H:%M"),
                "predicted": float(pred),
                "optimal": float(pred * 0.8)  # Simplified optimal usage
            }
            for date, pred in zip(future_dates, predictions)
        ]
    }

@app.get("/api/optimization-tips")
async def get_optimization_tips():
    current_data = {
        'timestamp': datetime.now(),
        'usage': 6.5
    }
    insights = optimizer.get_real_time_insights(current_data)
    return {"recommendations": insights['recommendations']}