from typing import List

from pydantic import AnyHttpUrl

BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://localhost:3000",
    "https://localhost:8000",
]
