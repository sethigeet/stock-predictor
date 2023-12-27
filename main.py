import uvicorn
import threading

from stock_predictor.agents import bureau

if __name__ == "__main__":
    threading.Thread(target=bureau.run, daemon=True).start()
    uvicorn.run(
        "stock_predictor.agents.api:app",
        host="0.0.0.0",
        port=5000,
        log_level="info",
    )
