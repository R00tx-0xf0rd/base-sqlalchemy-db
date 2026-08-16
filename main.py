import asyncio
import logging

from pydantic import create_model

from db.dao import BankDAO
from db.database import db_helper
from db.models import Bank
from db.schemas import BankBase

logger = logging.getLogger(__name__)


async def main():
    logger.info("starting program")
    async with db_helper.session_factory() as session:
        bank_filter = create_model("BankFilter", bank_name=(str, ...))(
            bank_name="Совкомбанк"
        )
        # bank_models = await BankDAO(session=session).get_all(filters=bank_filter)
        bank_models = await BankDAO(session=session).get_all()
        for bank in bank_models:
            logger.info("result: %s", bank.bank_name)
        # banks: list[Bank] = await BankDAO(session=session).get_all()
        # models = [BankBase.model_validate(bank) for bank in banks]
        # logger.debug(models)


if __name__ == "__main__":
    asyncio.run(main())
