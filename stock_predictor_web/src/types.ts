export type Stock = {
  Ticker: string;
  Name: string;
  Pct_Growth: number;
  Data: { [key: string]: number };
  Predicted_Data: { [key: string]: number };
};
