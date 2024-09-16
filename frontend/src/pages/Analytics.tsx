import React, { useState, useEffect } from 'react';
import { AnalyticsChart } from '../components/AnalyticsChart';
import { fetchAnalytics } from '../services/api';
import { useSelector, useDispatch } from '../store/analyticsSlice';

// HUMAN ASSISTANCE NEEDED
// The following component needs review and potential improvements for production readiness.
// The confidence level is below 0.8, indicating that some aspects may need refinement.

const Analytics: React.FC = () => {
  const [analyticsData, setAnalyticsData] = useState<any>(null);
  const dispatch = useDispatch();
  const { loading, error } = useSelector((state: any) => state.analytics);

  useEffect(() => {
    const getAnalyticsData = async () => {
      try {
        const data = await fetchAnalytics();
        setAnalyticsData(data);
        // Dispatch action to update Redux store if needed
        // dispatch(updateAnalytics(data));
      } catch (err) {
        console.error('Error fetching analytics data:', err);
        // Dispatch error action if needed
        // dispatch(setAnalyticsError(err.message));
      }
    };

    getAnalyticsData();
  }, [dispatch]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!analyticsData) return null;

  return (
    <div className="analytics-page">
      <h1>Analytics Dashboard</h1>
      
      {/* Render AnalyticsChart components for different metrics */}
      <AnalyticsChart data={analyticsData.userGrowth} title="User Growth" />
      <AnalyticsChart data={analyticsData.revenue} title="Revenue" />
      <AnalyticsChart data={analyticsData.engagement} title="User Engagement" />

      {/* Display summary statistics and trends */}
      <div className="summary-statistics">
        <h2>Summary Statistics</h2>
        <p>Total Users: {analyticsData.totalUsers}</p>
        <p>Monthly Active Users: {analyticsData.monthlyActiveUsers}</p>
        <p>Average Revenue Per User: ${analyticsData.averageRevenuePerUser}</p>
      </div>

      <div className="trends">
        <h2>Trends</h2>
        <ul>
          {analyticsData.trends.map((trend: string, index: number) => (
            <li key={index}>{trend}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Analytics;