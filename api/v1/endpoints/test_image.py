from fastapi import APIRouter, Query, Response
from services.image_service import ImageGenerationService

router = APIRouter()
image_service = ImageGenerationService()


@router.get(
    "/test-flux",
    response_class=Response,
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "Return generated image"
        }
    }
)
async def test_flux_generation(
    prompt: str = Query(...)
):
    image_bytes = await image_service.generate_flux_image(prompt)

    return Response(
        content=image_bytes,
        media_type="image/png"
    )