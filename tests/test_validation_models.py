import pytest
from pydantic import ValidationError

from eventyay_stripe.validation_models import PaymentInfoData


def test_payment_info_data_requires_charge_or_source():
    with pytest.raises(ValidationError):
        PaymentInfoData()


def test_payment_info_data_accepts_latest_charge_string():
    info = PaymentInfoData(latest_charge="ch_123")
    assert info.latest_charge == "ch_123"
    assert info.source is None


def test_payment_info_data_accepts_source_card_details():
    info = PaymentInfoData(source={"card": {"brand": "visa", "last4": "4242"}})
    assert info.source.card.brand == "visa"
    assert info.source.card.last4 == "4242"
