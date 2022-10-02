from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api import services, schemas
from deps import db_session

router = APIRouter()


@router.get('/shops')
async def list_shops(session: AsyncSession = db_session) -> list[schemas.Shop]:
    return [schemas.Shop.from_orm(obj) for obj in await services.list_shops(session)]


@router.get('/treats')
async def list_user_treats(user_id: int, session: AsyncSession = db_session) -> list[schemas.TreatOut]:
    return [schemas.TreatOut.from_orm(obj) for obj in await services.list_treats(session, user_id)]


@router.post('/treats', status_code=201)
async def create_treat(
        treat_input: schemas.TreatInput,
        user_id: int,
        session: AsyncSession = db_session,
) -> schemas.TreatOut:
    treat = await services.create_treat(session, treat_input.url, user_id)

    if not treat:
        raise HTTPException(status_code=404)
    return treat


@router.delete('/treats/{treat_id}', status_code=204)
async def delete_treat(treat_id: int, session: AsyncSession = db_session) -> None:
    await services.delete_treat_by_id(session, treat_id)
