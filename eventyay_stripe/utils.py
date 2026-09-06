def shredded_stripe_source(source) -> dict | None:
    """Keep only operational Stripe source fields. Ignore missing or null sources."""
    if not isinstance(source, dict):
        return None

    card = source.get("card")
    card_data = card if isinstance(card, dict) else {}
    return {
        "id": source.get("id"),
        "type": source.get("type"),
        "brand": source.get("brand"),
        "last4": source.get("last4"),
        "bank_name": source.get("bank_name"),
        "bank": source.get("bank"),
        "bic": source.get("bic"),
        "card": {
            "brand": card_data.get("brand"),
            "country": card_data.get("country"),
            "last4": card_data.get("last4"),
        },
    }


def shredded_stripe_payment_info(payload: dict) -> dict:
    """Build a privacy-safe copy of stored Stripe payment info."""
    new = {}
    source = shredded_stripe_source(payload.get("source"))
    if source is not None:
        new["source"] = source
    for key in ("amount", "currency", "status", "id"):
        if key in payload:
            new[key] = payload[key]
    new["_shredded"] = True
    return new
