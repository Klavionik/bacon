from fastapi import APIRouter, Depends, HTTPException

from .auth import get_current_user
from core.schemas import User, Shop, TreatOut
from core.repositories import TreatRepository, ShopRepository, ProductRepository, PriceRepository
from core.services import add_treat, TreatAlreadyExists
from ..deps import get_treat_repo, get_shop_repo, get_product_repo, get_price_repo
from .schemas import TreatInput

router = APIRouter()


@router.get('/shops')
async def list_shops(shop_service: ShopRepository = Depends(get_shop_repo)) -> list[Shop]:
    return await shop_service.list()


@router.get('/treats/user')
async def list_user_treats(
        user: User = Depends(get_current_user),
        treat_service: TreatRepository = Depends(get_treat_repo)
) -> list[TreatOut]:
    return await treat_service.list_by_user(user.id)


@router.post('/treats', status_code=201)
async def create_treat(
        treat_input: TreatInput,
        user: User = Depends(get_current_user),
        treat_repo: TreatRepository = Depends(get_treat_repo),
        shop_repo: ShopRepository = Depends(get_shop_repo),
        product_repo: ProductRepository = Depends(get_product_repo),
        price_repo: PriceRepository = Depends(get_price_repo),
) -> TreatOut:
    try:
        treat = await add_treat(
            user.id,
            treat_input.url,
            shop_repo,
            product_repo,
            price_repo,
            treat_repo
        )
    except TreatAlreadyExists:
        raise HTTPException(status_code=400, detail='Treat already exists.')
    return treat


@router.delete('/treats/{treat_id}', status_code=204)
async def delete_treat(
        treat_id: int,
        user: User = Depends(get_current_user),
        treat_service: TreatRepository = Depends(get_treat_repo),
) -> None:
    if not await treat_service.exists(treat_id, user.id):
        raise HTTPException(status_code=404)

    await treat_service.delete(treat_id)
    await treat_service.commit()
