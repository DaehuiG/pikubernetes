from fastapi import APIRouter

router = APIRouter(tags=['health'])

@router.get('/_health')
async def get_health():
    return {'status': 'Ok'}
