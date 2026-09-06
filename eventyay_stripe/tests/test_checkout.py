import datetime
import os

import pytest
from django.utils.crypto import get_random_string
from django.utils.timezone import now

if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    pytest.skip("Django settings are not configured", allow_module_level=True)

from eventyay.base.models import CartPosition, Event, Organizer, Product, ProductCategory, Quota


def add_cart_session(client, event, data):
    new_id = get_random_string(length=32)
    session = client.session
    session[f"current_cart_event_{event.pk}"] = new_id
    if "carts" not in session:
        session["carts"] = {}
    session["carts"][new_id] = data
    session.save()
    return new_id


def get_cart_session_key(client, event):
    cart_id = client.session.get(f"current_cart_event_{event.pk}")
    if cart_id:
        return cart_id
    return add_cart_session(client, event, {})


class MockedCharge:
    status = ""
    paid = False
    id = "ch_123345345"

    def refresh(self):
        pass


class Object:
    pass


class MockedPaymentintent:
    status = ""
    id = "pi_1EUon12Tb35ankTnZyvC3SdE"
    charges = Object()
    charges.data = [MockedCharge()]
    last_payment_error = None


@pytest.fixture
def env(client):
    orga = Organizer.objects.create(name="CCC", slug="ccc")
    event = Event.objects.create(
        organizer=orga,
        name="30C3",
        slug="30c3",
        date_from=datetime.datetime(now().year + 1, 12, 26, tzinfo=datetime.UTC),
        plugins="eventyay_stripe",
        live=True,
    )
    category = ProductCategory.objects.create(event=event, name="Everything", position=0)
    quota_tickets = Quota.objects.create(event=event, name="Tickets", size=5)
    ticket = Product.objects.create(
        event=event, name="Early-bird ticket", category=category, default_price=23, admission=True
    )
    quota_tickets.products.add(ticket)
    event.settings.set("attendee_names_asked", False)
    event.settings.set("payment_stripe__enabled", True)
    add_cart_session(client, event, {"email": "admin@localhost"})
    return client, ticket


@pytest.mark.django_db
@pytest.mark.skip(reason="Full checkout needs Eventyay multidomain/session setup beyond this plugin suite")
def test_payment(env, monkeypatch):
    def paymentintent_create(**kwargs):
        assert kwargs["amount"] == 1337
        assert kwargs["currency"] == "eur"
        assert kwargs["payment_method"] == "pm_189fTT2eZvKYlo2CvJKzEzeu"
        c = MockedPaymentintent()
        c.status = "succeeded"
        c.charges.data[0].paid = True
        paymentintent_create.called = True
        return c

    monkeypatch.setattr("stripe.PaymentIntent.create", paymentintent_create)

    client, ticket = env
    session_key = get_cart_session_key(client, ticket.event)
    CartPosition.objects.create(
        event=ticket.event,
        cart_id=session_key,
        product=ticket,
        price=13.37,
        expires=now() + datetime.timedelta(minutes=10),
    )
    client.get("/%s/%s/checkout/payment/" % (ticket.event.organizer.slug, ticket.event.slug), follow=True)
    client.post(
        "/%s/%s/checkout/questions/" % (ticket.event.organizer.slug, ticket.event.slug),
        {"email": "admin@localhost"},
        follow=True,
    )
    paymentintent_create.called = False
    response = client.post(
        "/%s/%s/checkout/payment/" % (ticket.event.organizer.slug, ticket.event.slug),
        {
            "payment": "stripe",
            "payment_method": "pm_189fTT2eZvKYlo2CvJKzEzeu",
            "stripe_card_brand": "visa",
            "stripe_card_last4": "1234",
        },
        follow=True,
    )
    assert not paymentintent_create.called
    assert response.status_code == 200
    assert "alert-danger" not in response.rendered_content
    response = client.post(
        "/%s/%s/checkout/confirm/" % (ticket.event.organizer.slug, ticket.event.slug), {}, follow=True
    )
    assert response.status_code == 200
