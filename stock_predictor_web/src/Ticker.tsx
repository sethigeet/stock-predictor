import { useParams } from "react-router-dom";
import { useQuery } from "react-query";

import { ErrorMsg, LoadingIndicator, StockChart } from "./components";

export default function Ticker() {
  const { ticker } = useParams();
  const { data, isLoading, isError, error } = useQuery(
    ["ticker", ticker?.toUpperCase() ?? null],
    async () =>
      fetch(
        `${import.meta.env.VITE_API_URL}/ticker/${ticker?.toUpperCase()}`
      ).then((res) => res.json()),
    {
      enabled: ticker !== undefined,
    }
  );

  return (
    <>
      <LoadingIndicator loading={isLoading} />
      {isError && <ErrorMsg error={error as Error} />}
      {!isLoading &&
        !isError &&
        (data === null ? (
          <div className="mx-auto grid place-items-center prose text-center mt-10">
            <h1>
              Unfortunately, we do not have data about that ticker right now!
            </h1>
          </div>
        ) : (
          <>
            <div className="stats shadow w-full bg-base-200">
              <div className="stat place-items-center">
                <div className="stat-title">{data.Name}</div>
                <div className="stat-value">{data.Ticker}</div>
                <div className="stat-desc">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    strokeWidth={1.5}
                    stroke="currentColor"
                    className="w-6 h-6"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M3.75 3v11.25A2.25 2.25 0 0 0 6 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0 1 18 16.5h-2.25m-7.5 0h7.5m-7.5 0-1 3m8.5-3 1 3m0 0 .5 1.5m-.5-1.5h-9.5m0 0-.5 1.5m.75-9 3-3 2.148 2.148A12.061 12.061 0 0 1 16.5 7.605"
                    />
                  </svg>
                </div>
              </div>

              <div className="stat place-items-center">
                <div className="stat-title">Expected Growth</div>
                <div
                  className={`stat-value ${
                    data.Pct_Growth > 0 ? "text-success" : "text-error"
                  }`}
                >
                  {data.Pct_Growth}%
                </div>
                <div
                  className={`stat-desc ${
                    data.Pct_Growth > 0 ? "text-success" : "text-error"
                  }`}
                >
                  (in a month from now)
                </div>
              </div>
            </div>
            <div className="max-w-3xl max-h-lg mx-auto mt-10">
              <StockChart
                dates={Object.keys(data.Data).map((k) => new Date(k))}
                prices={Object.values(data.Data)}
                dates_predicted={Object.keys(data.Predicted_Data).map(
                  (k) => new Date(k)
                )}
                prices_predicted={Object.values(data.Predicted_Data)}
              />
            </div>
          </>
        ))}
    </>
  );
}
