import { FC } from "react";

import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  Tooltip,
  CategoryScale,
  LinearScale,
} from "chart.js";
import { Line } from "react-chartjs-2";
ChartJS.register(
  LineElement,
  PointElement,
  Tooltip,
  CategoryScale,
  LinearScale
);

interface StockChartProps {
  dates: Date[];
  prices: number[];
  dates_predicted: Date[];
  prices_predicted: number[];
}

export const StockChart: FC<StockChartProps> = ({
  dates,
  prices,
  dates_predicted,
  prices_predicted,
}) => {
  return (
    <div>
      <Line
        datasetIdKey="id"
        data={{
          labels: [...dates, ...dates_predicted].map((date) =>
            date.toLocaleDateString()
          ),
          datasets: [
            {
              label: "Original",
              pointRadius: 0,
              data: [...prices, ...Array(prices_predicted.length).fill(NaN)],
              borderColor: "#7480ff",
              fill: false,
              tension: 0.4,
            },
            {
              label: "Predicted",
              pointRadius: 0,
              data: [
                ...Array(prices.length - 1).fill(NaN),
                prices[prices.length - 1],
                ...prices_predicted,
              ],
              borderColor: "#ffbe00",
              fill: false,
              tension: 0.4,
            },
          ],
        }}
        options={{
          responsive: true,
          interaction: {
            intersect: false,
          },
          plugins: {
            legend: {
              display: false,
            },
          },
          scales: {
            x: {
              grid: {
                display: false,
              },
            },
            y: {
              grid: {
                display: false,
              },
            },
          },
        }}
      />
    </div>
  );
};
