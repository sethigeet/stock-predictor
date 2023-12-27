import { FC } from "react";

export const Navbar: FC = () => {
  return (
    <nav className="navbar bg-primary text-primary-content">
      <div className="flex-1">
        <a className="btn btn-ghost text-xl uppercase">Stocks Predictor</a>
      </div>
      <div className="flex-none gap-2">
        <div className="form-control">
          <input
            type="text"
            placeholder="Enter a ticker"
            className="input input-bordered bg-indigo-700 w-24 md:w-auto text-white"
          />
        </div>
      </div>
    </nav>
  );
};
