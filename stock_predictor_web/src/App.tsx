import { Navbar, StockRow } from "./components";

export default function App() {
  return (
    <>
      <Navbar />
      <main className="max-w-4xl mx-auto flex flex-col justify-center prose mt-5">
        <h1 className="border-b-2 border-b-base-content self-center">
          Top Stocks of the Day
        </h1>
        <StockRow
          ticker="AAPL"
          name="Apple Inc."
          dates={[new Date(2021, 0, 1), new Date(2021, 0, 2)]}
          prices={[1, 2]}
          dates_predicted={[new Date(2021, 0, 3), new Date(2021, 0, 4)]}
          prices_predicted={[3, 5]}
        />
      </main>
    </>
  );
}
