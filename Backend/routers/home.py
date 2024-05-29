from fastapi import APIRouter

router = APIRouter(tags=['home'])

@router.get('/')
async def get_root():
    return {'name': 'Your-Backend-Service'}
