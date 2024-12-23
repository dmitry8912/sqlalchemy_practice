import uvicorn
from fastapi import FastAPI
from app.user import user_router
from app.order import order_router
from app.marketplace import marketplace_router

app = FastAPI()
app.include_router(user_router)
app.include_router(order_router)
app.include_router(marketplace_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, forwarded_allow_ips='*', proxy_headers=True)
