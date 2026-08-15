import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# Routers
from src.api.routers.health import router as health_router
from src.api.routers.companies import router as companies_router
from src.api.routers.sectors import router as sectors_router
from src.api.routers.documents import router as documents_router
from src.api.routers.valuation import router as valuation_router

from src.api.routers.portfolio import router as portfolio_router

from src.api.routers.screener import router as screener_router
from src.api.routers.peers import router as peers_router
# ------------------------------------------------
# FASTAPI APP
# ------------------------------------------------

app = FastAPI(
    title="Nifty100 Financial Intelligence API",
    description="API for Nifty100 Financial Intelligence Platform",
    version="1.0.0"
)


# ------------------------------------------------
# CORS
# ------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------------
# REQUEST LOGGING
# ------------------------------------------------

@app.middleware("http")
async def log_requests(request: Request, call_next):

    start_time = time.time()

    response = await call_next(request)

    process_time = round(
        time.time() - start_time,
        4
    )

    print(
        f"{request.method} "
        f"{request.url.path} "
        f"{response.status_code} "
        f"{process_time}s"
    )

    return response


# ------------------------------------------------
# ROUTERS
# ------------------------------------------------

app.include_router(
    health_router,
    prefix="/api/v1"
)

app.include_router(
    screener_router,
    prefix="/api/v1"
)
app.include_router(
    valuation_router,
    prefix="/api/v1"
)

app.include_router(
    companies_router,
    prefix="/api/v1"
)
app.include_router(
    sectors_router,
    prefix="/api/v1"
)

app.include_router(
    portfolio_router,
    prefix="/api/v1"
)
app.include_router(
    documents_router,
    prefix="/api/v1"
)






app.include_router(
    peers_router,
    prefix="/api/v1"
)
# ------------------------------------------------
# ROOT ENDPOINT
# ------------------------------------------------

@app.get("/")
def root():
    """API root endpoint."""

    return {
        "message": "Nifty100 Financial Intelligence API is running"
    }