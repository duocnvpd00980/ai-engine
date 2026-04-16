import sys
import os
# Thêm dòng này để Python tìm thấy các module trong thư mục app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from api.v1.endpoints import banner
import uvicorn

app = FastAPI(title="Banner Generator")

app.include_router(banner.router, prefix="/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)