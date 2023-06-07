from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api import schemas, services
from auth import get_user
from auth.schemas import UserRead
from deps import db_session, shop_client
from perekrestok.client import PerekrestokClient
from storage.models import User

router = APIRouter()


@router.get("/shops", response_model=list[schemas.Shop])
async def list_shops(session: AsyncSession = Depends(db_session)):
    return await services.list_shops(session)


@router.get(
    "/user_products", response_model=list[schemas.UserProductOutput], response_model_by_alias=False
)
async def list_user_products(
    user: User = Depends(get_user), session: AsyncSession = Depends(db_session)
):
    return await services.list_user_products(session, user.id)


@router.post(
    "/user_products",
    status_code=201,
    response_model=schemas.UserProductOutput,
    response_model_by_alias=False,
)
async def create_user_product(
    user_product_input: schemas.UserProductInput,
    user: UserRead = Depends(get_user),
    session: AsyncSession = Depends(db_session),
):
    user_product = await services.create_user_product(session, user_product_input.url, user.id)

    if not user_product:
        raise HTTPException(status_code=404)
    return user_product


@router.delete("/user_products/{user_product_id}", status_code=204)
async def delete_user_product(
    user_product_id: int, session: AsyncSession = Depends(db_session)
) -> None:
    await services.delete_user_product_by_id(session, user_product_id)


@router.get(
    "/shops/{shop_id}/locations/search",
    response_model=list[schemas.ShopLocationSuggestion],
)
async def search_shop_locations(
    shop_id: int, address: str, client: PerekrestokClient = shop_client
):
    async with client:
        coordinates = await client.get_location_coordinates(address)

        if not coordinates:
            return []

        shop_locations = await client.get_shops_by_coordinates(coordinates)

    result = [
        schemas.ShopLocationSuggestion(
            address=obj["address"], title=obj["title"], shop_id=shop_id, external_id=obj["id"]
        )
        for obj in shop_locations
    ]

    return result


@router.get("/user/{user_id}/shop-locations", response_model=list[schemas.ShopLocation])
async def get_user_shop_locations(
    user: UserRead = Depends(get_user), session: AsyncSession = Depends(db_session)
):
    locations = await services.get_user_shop_locations_by_user(session, user.id)
    return locations


@router.put(
    "/user/{user_id}/shop-locations",
    response_model=list[schemas.ShopLocationSuggestion],
    status_code=201,
)
async def save_user_shop_locations(
    locations: list[schemas.ShopLocationSuggestion],
    user: UserRead = Depends(get_user),
    session: AsyncSession = Depends(db_session),
):
    return await services.save_user_shop_locations(session, user.id, locations)
