import logging
from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy import Result, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Base

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=Base)


class BaseDAO[T]:
    model: type[T] | None = None

    def __init__(self, session: AsyncSession):
        self._session = session
        if not self.model:
            raise ValueError("Model must be defined in a child class")

    async def get_model_by_id(self, model_id: int) -> T | None:
        if self.model is None:
            raise ValueError("Model is not defined")
        try:
            query = select(self.model).filter_by(id=model_id)
            if result := await self._session.execute(query):
                return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.info("No model with id: %s, error: %s", model_id, e)
            raise

    async def get_all(self, filters: BaseModel) -> list[T]:
        filter_dict = filters.model_dump(exclude_unset=True) if filters else {}
        if self.model is None:
            raise ValueError("Model is not defined")
        try:
            query = select(self.model).filter_by(**filter_dict)
            result: Result = await self._session.execute(query)
            items = result.scalars().all()
            return list(items)
        except SQLAlchemyError:
            logger.info("Error fetching all data")
            raise
