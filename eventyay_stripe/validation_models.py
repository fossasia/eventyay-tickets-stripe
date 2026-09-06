from pydantic import BaseModel, model_validator


class CardDetails(BaseModel):
    brand: str | None = None
    last4: str | None = None
    exp_month: int | None = None
    exp_year: int | None = None


class IdealDetails(BaseModel):
    bank: str | None = None


class BancontactDetails(BaseModel):
    bankname: str | None = None


class SofortDetails(BaseModel):
    country: str | None = None
    iban_last4: str | None = None
    bank_name: str | None = None


class EPSDetails(BaseModel):
    bank: str | None = None


class P24Details(BaseModel):
    bank: str | None = None


class PaymentMethodDetails(BaseModel):
    card: CardDetails | None = None
    ideal: IdealDetails | None = None
    bancontact: BancontactDetails | None = None
    sofort: SofortDetails | None = None
    eps: EPSDetails | None = None
    p24: P24Details | None = None


class LatestCharge(BaseModel):
    payment_method_details: PaymentMethodDetails | None = None


class Source(BaseModel):
    card: CardDetails | None = None
    ideal: IdealDetails | None = None
    bancontact: BancontactDetails | None = None
    sofort: SofortDetails | None = None
    eps: EPSDetails | None = None
    p24: P24Details | None = None


class PaymentInfoData(BaseModel):
    latest_charge: str | LatestCharge | None = None
    source: Source | None = None

    @model_validator(mode="before")
    def check_latest_charge_or_source(cls, values):
        latest_charge = values.get("latest_charge")
        source = values.get("source")
        if not latest_charge and not source:
            raise ValueError("Either 'latest_charge' or 'source' must be provided.")
        return values
