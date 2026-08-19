import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from db.base_dao import BaseDAO
from db.models import Bank

logger = logging.getLogger(__name__)


class BankDAO(BaseDAO[Bank]):
    model: type[Bank] = Bank

    async def get_model_by_id(self, model_id: int) -> Bank | None:
        if self.model is None:
            raise ValueError("Model is not defined")
        try:
            query = (
                select(self.model)
                .options(selectinload(Bank.rates))
                .filter_by(id=model_id)
            )
            if result := await self._session.execute(query):
                return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.info("No model with id: %s, error: %s", model_id, e)
            raise
