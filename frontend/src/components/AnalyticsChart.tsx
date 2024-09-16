import React from 'react';
import { Chart } from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';
import { AnalyticsData } from '../schema/types';

// HUMAN ASSISTANCE NEEDED
// The confidence level is below 0.8, and the component might need additional refinement for production readiness.
// Please review and enhance the following areas:
// - Error handling for invalid chart types
// - Responsive design considerations
// - Accessibility features
// - Performance optimization for large datasets

const AnalyticsChart: React.FC<{ data: AnalyticsData; chartType: string }> = ({ data, chartType }) => {
  const processData = (data: AnalyticsData) => {
    // Process input data for chart format
    const labels = data.map(item => item.label);
    const values = data.map(item => item.value);
    return { labels, datasets: [{ data: values, label: 'Analytics' }] };
  };

  const chartData = processData(data);

  const chartConfig = {
    responsive: true,
    plugins: {
      tooltip: {
        mode: 'index',
        intersect: false,
      },
      legend: {
        position: 'top' as const,
      },
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'Time',
        },
      },
      y: {
        display: true,
        title: {
          display: true,
          text: 'Value',
        },
      },
    },
  };

  const renderChart = () => {
    switch (chartType.toLowerCase()) {
      case 'line':
        return <Line data={chartData} options={chartConfig} />;
      case 'bar':
        return <Bar data={chartData} options={chartConfig} />;
      default:
        return <div>Unsupported chart type</div>;
    }
  };

  return (
    <div className="analytics-chart">
      {renderChart()}
    </div>
  );
};

export default AnalyticsChart;