from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import centers, resources

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "resource-service"}

@app.get("/")
def root():
    return {"message": "Welcome to Resource Service"}

app.include_router(centers.router, prefix=f"{settings.API_V1_STR}/centers", tags=["centers"])
app.include_router(resources.router, prefix=f"{settings.API_V1_STR}/resources", tags=["resources"])

