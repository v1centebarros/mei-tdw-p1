from fastapi import APIRouter

from services.categories import CategoryService

categories_service = CategoryService()

router = APIRouter(tags=['Categories'])

@router.get("/categories/")
async def get_all_categories():
    """
    Get all available categories
    """
    return categories_service.get_all_categories()
