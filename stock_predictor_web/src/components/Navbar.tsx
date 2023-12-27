import { FC, useState } from "react";

import { useNavigate } from "react-router-dom";

export const Navbar: FC = () => {
  const navigate = useNavigate();
  const [ticker, setTicker] = useState("");

  return (
    <nav className="navbar bg-primary text-primary-content">
      <div className="flex-1">
        <a className="btn btn-ghost text-xl uppercase">Stocks Predictor</a>
      </div>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          navigate(`/ticker/${ticker}`);
        }}
        className="flex-none gap-2"
      >
        <div className="form-control">
          <input
            type="text"
            placeholder="Enter a ticker"
            className="input input-bordered bg-indigo-700 w-24 md:w-auto text-white"
            value={ticker}
            onChange={(e) => setTicker(e.currentTarget.value)}
          />
        </div>
      </form>
    </nav>
  );
};
