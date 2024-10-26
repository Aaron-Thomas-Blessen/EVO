// frontend/src/components/EnergyDashboard.jsx
import React, { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { Battery, Zap, TrendingDown, AlertCircle } from "lucide-react";

const EnergyDashboard = () => {
  const [data, setData] = useState([]);
  const [currentStatus, setCurrentStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          "http://localhost:8000/api/current-status"
        );
        const result = await response.json();
        setData(result.predictions);
        setCurrentStatus(result.current_status);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching data:", error);
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 60000); // Update every minute
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  const predictedSavings = currentStatus
    ? (
        (currentStatus.current_usage - currentStatus.expected_usage) *
        0.15
      ).toFixed(2)
    : "0.00";

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Smart Energy Optimizer</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="p-4 border rounded-lg">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium">Current Usage</h3>
            <Battery className="text-blue-500" />
          </div>
          <div className="text-2xl font-bold">
            {currentStatus?.current_usage.toFixed(1)} kWh
          </div>
        </div>

        <div className="p-4 border rounded-lg">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium">Potential Savings</h3>
            <Zap className="text-yellow-500" />
          </div>
          <div className="text-2xl font-bold">${predictedSavings}</div>
        </div>

        <div className="p-4 border rounded-lg">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium">Optimization Score</h3>
            <TrendingDown className="text-green-500" />
          </div>
          <div className="text-2xl font-bold">
            {currentStatus?.efficiency_score}/100
          </div>
        </div>
      </div>

      <div className="mb-6 p-4 border rounded-lg">
        <h2 className="text-lg font-semibold mb-4">Energy Usage Analysis</h2>
        <LineChart width={700} height={300} data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="predicted"
            stroke="#2563eb"
            name="Predicted Usage"
          />
          <Line
            type="monotone"
            dataKey="optimal"
            stroke="#16a34a"
            name="Optimal Usage"
          />
        </LineChart>
      </div>

      {currentStatus?.recommendations.map((rec, index) => (
        <div key={index} className="mb-4 p-4 border rounded-lg bg-blue-50">
          <div className="flex items-center gap-2">
            <AlertCircle className="h-4 w-4 text-blue-500" />
            <span>{rec.message}</span>
          </div>
          <div className="mt-2 text-sm text-blue-600">
            Potential savings: {rec.potential_savings}
          </div>
        </div>
      ))}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <button className="p-2 bg-blue-500 text-white rounded-lg">
          Generate Optimization Report
        </button>
        <button className="p-2 border border-blue-500 text-blue-500 rounded-lg">
          Configure Alerts
        </button>
      </div>
    </div>
  );
};

export default EnergyDashboard;
