import sys
import os

# FIX IMPORT PATH (an toàn hơn)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from fastapi import FastAPI
from api.v1.endpoints import banner
from services.image_service import ImageGenerationService
import uvicorn
import logging
from api.v1.endpoints import test_canvas


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

app = FastAPI(title="Banner Generator")

# =========================
# SERVICE INIT (SAFE)
# =========================
image_service = None


@app.on_event("startup")
async def startup_event():
    global image_service
    image_service = ImageGenerationService()


# =========================
# ROUTER
# =========================
app.include_router(banner.router, prefix="/v1")
app.include_router(test_canvas.router, prefix="/v1")

# =========================
# TEST IMAGE ENDPOINT
# =========================
@app.get("/v1/test-image")
async def test_image(prompt: str):
    global image_service

    url = await image_service.generate_flux_image(prompt)
    return {
        "status": "success",
        "prompt": prompt,
        "image_url": url
    }


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000
        # ❌ KHÔNG bật reload ở đây
    )