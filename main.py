import asyncio
import logging

from pydantic import create_model
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.database import db_helper
from db.ext_dao import BankDAO
from db.models import Bank
from db.schemas import BankBase

logger = logging.getLogger(__name__)


async def get_bank_with_rates(session: AsyncSession, bank_id: int):
    query = select(Bank).options(selectinload(Bank.rates)).where(Bank.id == bank_id)
    try:
        bank_data = await session.scalar(query)
    except SQLAlchemyError:
        logger.error("Error fetching data for Bank ID %s", bank_id)
    return bank_data


async def main():
    logger.info("starting program")
    async with db_helper.session_factory() as session:
        # bank_data = await get_bank_with_rates(session, 1)
        bank_filter = create_model("BankFilter", bank_name=(str, ...))(
            bank_name="Совкомбанк"
        )
        bank_model = await BankDAO(session=session).get_model_by_id(model_id=22)
        for rate in bank_model.rates:
            print(rate)
        bank_models = await BankDAO(session=session).get_all(filters=bank_filter)
        # bank_models = await BankDAO(session=session).get_all()
        for bank in bank_models:
            logger.info("result: %s", bank.bank_name)
        # banks: list[Bank] = await BankDAO(session=session).get_all()
        # models = [BankBase.model_validate(bank) for bank in banks]
        # logger.debug(models)


if __name__ == "__main__":
    asyncio.run(main())
