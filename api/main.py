from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import get_settings
from core.minio import init_minio
from db.database import engine
from models.file import Base
from routers import auth, file, search, categories, chat

# Load environment variables
load_dotenv()

settings = get_settings()

tags_metadata = [
    {
        "name": "File Management",
        "description": "File operations"
    },
    {
        "name": "Authentication",
        "description": "Operations related to authentication using Keycloak"
    },
    {
        "name": "Search",
        "description": "Search operations"
    },
    {
        "name": "Categories",
        "description": "Operations related to categories"
    }
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/api/docs",
    openapi_tags=tags_metadata
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

init_minio()

app.include_router(prefix="/api", router=auth.router)
app.include_router(prefix="/api", router=file.router)
app.include_router(prefix="/api", router=search.router)
app.include_router(prefix="/api", router=categories.router)
app.include_router(prefix="/api", router=chat.router)
