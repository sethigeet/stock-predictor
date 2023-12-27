from stock_predictor.agents import bureau
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "stock_predictor.agents.api:app",
        host="0.0.0.0",
        port=5000,
        log_level="info",
    )
    bureau.run()
