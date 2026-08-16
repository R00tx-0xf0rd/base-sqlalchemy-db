from pydantic import BaseModel, ConfigDict


class BankBase(BaseModel):
    bank_name: str
    bank_url: str

    model_config = ConfigDict(from_attributes=True)
