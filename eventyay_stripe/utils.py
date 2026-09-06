import hashlib
import hmac
import re
import time


def stripe_key_is_valid(value: str, prefixes: list[str]) -> bool:
    """Return True when a Stripe key starts with one of the expected prefixes."""
    return any(value.startswith(prefix) for prefix in prefixes)


def stripe_statement_descriptor(event_slug: str, order_code: str, event_name: object, length: int = 22) -> str:
    """Build a Stripe statement descriptor from event and order identifiers."""
    eventname = re.sub("[^a-zA-Z0-9 ]", "", str(event_name))
    return f"{event_slug.upper()}-{order_code} {eventname}"[:length]


def stripe_decimal_to_int(amount, places: int) -> int:
    """Convert a decimal amount to Stripe's integer minor units."""
    return int(amount * 10**places)


def stripe_webhook_signature_header(payload: str, secret: str, timestamp: int | None = None) -> str:
    """Build a Stripe-Signature header value for webhook tests."""
    timestamp = timestamp if timestamp is not None else int(time.time())
    signed_payload = f"{timestamp}.{payload}"
    signature = hmac.new(secret.encode("utf-8"), signed_payload.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"t={timestamp},v1={signature}"
