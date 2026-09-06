from eventyay_stripe.utils import shredded_stripe_payment_info, shredded_stripe_source


def test_shredded_stripe_source_ignores_null_and_non_dicts():
    assert shredded_stripe_source(None) is None
    assert shredded_stripe_source("src_123") is None
    assert shredded_stripe_source([]) is None


def test_shredded_stripe_source_keeps_operational_fields():
    source = shredded_stripe_source(
        {
            "id": "src_1",
            "type": "card",
            "brand": "Visa",
            "last4": "4242",
            "card": {"brand": "Visa", "country": "US", "last4": "4242", "exp_year": 2030},
            "customer": "cus_secret",
        }
    )
    assert source["id"] == "src_1"
    assert source["card"]["country"] == "US"
    assert "customer" not in source
    assert "exp_year" not in source["card"]


def test_shredded_stripe_source_accepts_null_card():
    source = shredded_stripe_source({"id": "src_1", "type": "card", "card": None})
    assert source["id"] == "src_1"
    assert source["card"] == {"brand": None, "country": None, "last4": None}


def test_shredded_stripe_payment_info_with_null_source():
    shredded = shredded_stripe_payment_info(
        {
            "id": "pi_1",
            "amount": 1337,
            "currency": "eur",
            "status": "succeeded",
            "source": None,
            "client_secret": "secret",
        }
    )
    assert "source" not in shredded
    assert shredded["id"] == "pi_1"
    assert shredded["amount"] == 1337
    assert shredded["_shredded"] is True
    assert "client_secret" not in shredded


def test_shredded_stripe_payment_info_with_legacy_source():
    shredded = shredded_stripe_payment_info(
        {
            "id": "ch_1",
            "source": {
                "id": "src_1",
                "type": "card",
                "card": {"brand": "Visa", "country": "DE", "last4": "4242"},
            },
        }
    )
    assert shredded["source"]["card"]["country"] == "DE"
    assert shredded["_shredded"] is True
