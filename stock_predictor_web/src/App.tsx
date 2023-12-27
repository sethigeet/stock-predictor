import { useQuery } from "react-query";
import { ErrorMsg, LoadingIndicator, StockRow } from "./components";

import type { Stock } from "./types";

export default function App() {
  const { data, isLoading, isError, error } = useQuery(
    "top-tickers",
    async () =>
      fetch(`${import.meta.env.VITE_API_URL}/top-tickers`).then((res) =>
        res.json()
      )
  );

  return (
    <>
      <LoadingIndicator loading={isLoading} />
      {isError && <ErrorMsg error={error as Error} />}
      {data && (
        <main className="max-w-5xl mx-auto flex flex-col justify-center prose mt-5">
          <h1 className="border-b-2 border-b-base-content self-center">
            Top Stocks of the Day
          </h1>
          {data.map((stock: Stock) => (
            <div className="my-3" key={stock.Ticker}>
              <StockRow
                ticker={stock.Ticker}
                name={stock.Name}
                pctGrowth={stock.Pct_Growth}
                dates={Object.keys(stock.Data).map((k) => new Date(k))}
                prices={Object.values(stock.Data)}
                datesPredicted={Object.keys(stock.Predicted_Data).map(
                  (k) => new Date(k)
                )}
                pricesPredicted={Object.values(stock.Predicted_Data)}
              />
            </div>
          ))}
        </main>
      )}
    </>
  );
}
