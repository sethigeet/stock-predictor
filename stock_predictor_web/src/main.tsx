import React from "react";
import ReactDOM from "react-dom/client";

import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { QueryClient, QueryClientProvider } from "react-query";

import App from "./App.tsx";
import Ticker from "./Ticker.tsx";
import NotFound from "./NotFound.tsx";
import "./globals.css";

import { Navbar } from "./components/Navbar.tsx";

const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="/ticker">
            <Route index element={<Navigate to="/" replace />} />
            <Route path=":ticker" element={<Ticker />} />
          </Route>
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Router>
    </QueryClientProvider>
  </React.StrictMode>
);
