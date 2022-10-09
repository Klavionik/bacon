from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api import services, schemas
from deps import db_session, shop_client
from perekrestok.client import PerekrestokClient

router = APIRouter()


@router.get('/shops', response_model=list[schemas.Shop])
async def list_shops(session: AsyncSession = db_session):
    return await services.list_shops(session)


@router.get('/treats', response_model=list[schemas.TreatOut], response_model_by_alias=False)
async def list_user_treats(user_id: int, session: AsyncSession = db_session):
    return await services.list_treats(session, user_id)


@router.post('/treats', status_code=201, response_model=schemas.TreatOut, response_model_by_alias=False)
async def create_treat(
        treat_input: schemas.TreatInput,
        user_id: int,
        session: AsyncSession = db_session,
):
    treat = await services.create_treat(session, treat_input.url, user_id)

    if not treat:
        raise HTTPException(status_code=404)
    return treat


@router.delete('/treats/{treat_id}', status_code=204)
async def delete_treat(treat_id: int, session: AsyncSession = db_session) -> None:
    await services.delete_treat_by_id(session, treat_id)


@router.get(
    '/shops/{shop_id}/locations/search',
    response_model=list[schemas.ShopLocationSuggestion],
)
async def search_shop_locations(shop_id: int, address: str, client: PerekrestokClient = shop_client):
    async with client:
        coordinates = await client.get_location_coordinates(address)

        if not coordinates:
            return []

        shop_locations = await client.get_shops_by_coordinates(coordinates)

    result = [schemas.ShopLocationSuggestion(
        address=obj['address'],
        title=obj['title'],
        shop_id=shop_id,
        external_id=obj['id']
    ) for obj in shop_locations]

    return result


@router.get('/users/me', response_model=schemas.User)
async def get_current_user(session: AsyncSession = db_session):
    # For now, return user with ID 1.
    return await services.get_user(session, user_id=1)


@router.get('/user/{user_id}/shop-locations', response_model=list[schemas.ShopLocation])
async def get_user_shop_locations(user_id: int, session: AsyncSession = db_session):
    locations = await services.get_user_shop_locations_by_user(session, user_id)
    return locations


@router.put('/user/{user_id}/shop-locations', response_model=list[schemas.ShopLocationSuggestion], status_code=201)
async def save_user_shop_locations(
        user_id: int,
        locations: list[schemas.ShopLocationSuggestion],
        session: AsyncSession = db_session
):
    return await services.save_user_shop_locations(session, user_id, locations)
