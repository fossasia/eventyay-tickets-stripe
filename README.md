Eventyay Stripe
===============

Eventyay Stripe is a payment plugin for `Eventyay <https://github.com/fossasia/eventyay>`_. It allows event organisers to accept payments through `Stripe <https://stripe.com>`_ and Stripe supported payment methods.

The plugin adds Stripe based payment providers to Eventyay. It supports direct Stripe API keys, Stripe Connect, live and test mode configuration, Payment Intents, Strong Customer Authentication flows, webhook based payment updates, refunds, partial refunds, organiser payment settings, Apple Pay domain verification, and payment data shredding for privacy related workflows.

Project status
--------------

Eventyay Stripe is maintained as part of the Eventyay plugin ecosystem.

The package is named ``eventyay-stripe`` and the Python module is named ``eventyay_stripe``.

The current package metadata reads the version from ``eventyay_stripe.__version__``. At the time this README was prepared, the module version was ``1.0.1``.

Main features
-------------

- Stripe payment support for Eventyay events
- Credit card payments through Stripe
- Stripe Connect support for connecting organiser Stripe accounts
- Live and test endpoint handling
- Payment Intents based payment processing
- Strong Customer Authentication and return flow handling
- Webhook handling for Stripe payment events
- Refund and partial refund support
- Support for externally reported refunds and disputes
- Apple Pay domain verification task
- Payment data shredding for sensitive payment information
- Organiser and event level Stripe settings
- Stripe Connect application fee settings
- Internationalisation support through Django translation files

Supported payment methods
-------------------------

The plugin registers multiple Stripe backed payment providers. Availability can depend on event currency, Stripe account configuration, payment method support in the organiser country, and Stripe account settings.

Supported methods include:

- Credit card
- iDEAL
- Alipay
- Bancontact
- SOFORT
- EPS
- Multibanco
- Przelewy24
- WeChat Pay
- PayPal via Stripe
- Revolut Pay
- SEPA Direct Debit
- Swish
- TWINT
- MobilePay
- Affirm
- Klarna

Requirements
------------

- Python 3.9 or newer
- A working Eventyay development or production setup
- A Stripe account
- Stripe API keys or Stripe Connect configuration
- The Python package ``stripe==11.3.*``

Installation for development
----------------------------

Use this setup when developing the plugin together with a local Eventyay installation.

1. Set up Eventyay
~~~~~~~~~~~~~~~~~~

First make sure you have a working Eventyay development setup.

See the Eventyay repository:

`https://github.com/fossasia/eventyay <https://github.com/fossasia/eventyay>`_

2. Clone this repository
~~~~~~~~~~~~~~~~~~~~~~~~

Clone the plugin repository next to your Eventyay checkout or into the local plugin directory used by your Eventyay development setup.

.. code-block:: bash

   git clone https://github.com/fossasia/eventyay-stripe.git
   cd eventyay-stripe

3. Activate the Eventyay virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Activate the virtual environment used by your Eventyay installation.

Example:

.. code-block:: bash

   cd ../eventyay/app
   . .venv/bin/activate

4. Install the plugin in editable mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From the ``eventyay-stripe`` directory, install the plugin in editable mode.

.. code-block:: bash

   pip install -e ".[dev]"

If your Eventyay development setup uses ``uv``, you can also use:

.. code-block:: bash

   uv pip install -e ".[dev]"

5. Apply migrations
~~~~~~~~~~~~~~~~~~~

Run migrations from the Eventyay app directory.

.. code-block:: bash

   python manage.py migrate

6. Compile translations
~~~~~~~~~~~~~~~~~~~~~~~

Compile translation files from the plugin directory.

.. code-block:: bash

   make

7. Restart Eventyay
~~~~~~~~~~~~~~~~~~~

Restart the Eventyay development server and worker processes if they are running.

.. code-block:: bash

   python manage.py runserver

If you use Docker for Eventyay development, restart the relevant containers after installing or changing the plugin.

Using the plugin
----------------

1. Open the Eventyay organiser interface.
2. Open the event where Stripe payments should be enabled.
3. Go to the payment provider settings.
4. Enable Stripe in the payment settings.
5. Configure Stripe API keys or connect an account through Stripe Connect.
6. Select the payment methods that should be available for the event.
7. Save the payment settings.
8. Place a test order before enabling the payment method for a live event.

Stripe configuration
--------------------

The plugin can be used with direct Stripe keys or Stripe Connect.

For direct key configuration, organisers configure Stripe keys in the payment provider settings. The plugin validates key prefixes for publishable and secret keys.

For Stripe Connect, the platform administrator configures global Stripe Connect settings. Organisers can then connect their Stripe account from the Eventyay interface. The plugin stores account identifiers and related publishable keys in the event payment settings.

Important configuration areas include:

- Publishable key
- Secret key
- Merchant country
- Stripe Connect Client ID
- Stripe Connect live and test keys
- Stripe Connect application fee percentage
- Stripe Connect minimum and maximum application fee
- Stripe Connect destination account settings where applicable

Test mode
---------

The plugin supports Stripe test mode. If an event is in test mode, the plugin uses Stripe test API settings where available.

Use test mode before enabling Stripe payments for a live event. Stripe test cards can be used to verify checkout, Strong Customer Authentication, webhook handling, and refund flows.

Checkout flow
-------------

During checkout, the plugin prepares the selected Stripe payment method and creates a Stripe Payment Intent for the Eventyay order payment amount and event currency.

The Payment Intent stores Eventyay metadata such as the order ID, event ID, and order code. The plugin records the Stripe Payment Intent reference so later webhook notifications can be mapped back to the corresponding Eventyay order and payment.

If Stripe requires additional customer action, the plugin redirects through the Strong Customer Authentication flow and returns to Eventyay afterwards.

Webhook flow
------------

The plugin exposes Stripe webhook endpoints for payment provider notifications.

The webhook handler verifies the Stripe signature, reads the event object, maps known Stripe objects back to Eventyay orders and payments, and processes relevant updates.

Handled Stripe object categories include:

- ``charge``
- ``dispute``
- ``source``
- ``payment_intent``

Webhook processing is used for asynchronous payment status updates, externally reported refunds, disputes, and charge related events.

Refunds
-------

The plugin supports refunds and partial refunds through the Stripe API.

When a refund is executed, the plugin finds the Stripe charge connected to the stored payment information and creates a Stripe refund. If Stripe reports an error during refund processing, the plugin marks the refund as failed and raises an Eventyay payment exception so the organiser can see that the refund could not be completed automatically.

URLs
----

The plugin registers event specific and global URLs for Stripe payment handling.

Event URLs include:

.. code-block:: text

   /<organizer>/<event>/stripe/webhook/
   /<organizer>/<event>/stripe/redirect/
   /<organizer>/<event>/stripe/return/<order>/<hash>/<payment>/
   /<organizer>/<event>/stripe/sca/<order>/<hash>/<payment>/
   /<organizer>/<event>/stripe/sca/<order>/<hash>/<payment>/return/

Control and global URLs include:

.. code-block:: text

   /control/event/<organizer>/<event>/stripe/disconnect/
   /control/organizer/<organizer>/stripeconnect/
   /_stripe/webhook/
   /_stripe/oauth_return/

Data model
----------

The plugin stores Stripe references in ``ReferencedStripeObject``.

The model links the external Stripe reference to:

- The Eventyay order
- The Eventyay payment, if available

This allows webhook notifications to be mapped back to the corresponding Eventyay order and payment.

The plugin also stores Apple Pay domain verification records in ``RegisteredApplePayDomain``.

Development commands
--------------------

Run these commands from the plugin repository unless otherwise noted.

Install the plugin in editable mode:

.. code-block:: bash

   pip install -e ".[dev]"

Lint and format Python with Ruff:

.. code-block:: bash

   ruff check .
   ruff check . --fix
   ruff format --check .
   ruff format .

Run standalone plugin tests:

.. code-block:: bash

   pytest tests/

Django integration tests in ``eventyay_stripe/tests`` require a working Eventyay install and are skipped when Eventyay is not available.

Compile translations:

.. code-block:: bash

   make

Regenerate translation files:

.. code-block:: bash

   make localegen

Package structure
-----------------

Important files and directories:

.. code-block:: text

   .
   ├── docs/                  Additional documentation
   ├── eventyay_stripe/
   │   ├── __init__.py        Plugin version
   │   ├── apps.py            Eventyay plugin metadata
   │   ├── forms.py           Settings forms and key validation
   │   ├── models.py          Stripe reference and Apple Pay domain models
   │   ├── payment.py         Payment provider implementations
   │   ├── signals.py         Payment provider registration and settings hooks
   │   ├── tasks.py           Background tasks such as Apple Pay domain verification
   │   ├── urls.py            Event, control, webhook, OAuth, and SCA URLs
   │   ├── utils.py           Shared Stripe helpers
   │   ├── views.py           Webhook, OAuth, redirect, return, and settings views
   │   ├── templates/         Django templates
   │   ├── static/            Static assets
   │   ├── locale/            Translation files
   │   └── migrations/        Database migrations
   ├── pyproject.toml         Python package metadata
   ├── setup.py               Setuptools entry point
   ├── MANIFEST.in            Package data inclusion
   ├── Makefile               Translation helper commands
   ├── pytest.ini             Pytest configuration
   ├── tests/                 Standalone plugin tests
   ├── LICENSE                Apache License 2.0
   └── README.rst             Project documentation

Packaging
---------

The package metadata is defined in ``pyproject.toml``.

The package includes:

- Python module ``eventyay_stripe``
- Static files
- Templates
- Locale files
- Database migrations
- License file

The version is read from ``eventyay_stripe.__version__``.

Security and privacy notes
--------------------------

The plugin stores payment provider responses as payment information in Eventyay.

The plugin includes a ``shred_payment_info`` implementation that keeps selected operational fields and masks sensitive data. It also shreds related Stripe log entry data where applicable.

Production notes
----------------

Before using the plugin for a live event:

- Test the Stripe connection with a test event.
- Verify that the payment methods appear correctly in checkout.
- Confirm that the Stripe webhook endpoint is reachable from Stripe.
- Configure the Stripe webhook signing secret in the Eventyay deployment.
- Place a test order and verify that payment confirmation updates the order.
- Test Strong Customer Authentication return flows.
- Test refund and partial refund handling before relying on automatic refunds.
- Confirm that each enabled payment method is available for the event currency and organiser country.
- Confirm that Apple Pay domain verification works if Apple Pay is expected to be available through card payments.
- Review Stripe Connect fee settings if the platform uses connected accounts.

License
-------

Eventyay Stripe is released under the terms of the Apache License 2.0.

See `LICENSE <LICENSE>`_ for the full license text.

Links
-----

- `Eventyay <https://github.com/fossasia/eventyay>`_
- `Eventyay Stripe <https://github.com/fossasia/eventyay-stripe>`_
- `Stripe <https://stripe.com>`_
- `Stripe Python package <https://pypi.org/project/stripe/>`_
- `FOSSASIA <https://fossasia.org>`_
