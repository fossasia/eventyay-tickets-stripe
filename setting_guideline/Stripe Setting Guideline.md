# Stripe Payment Settings Instruction

This guide will walk you through obtaining the necessary keys to integrate Stripe with your application.  To get started, you'll need an active Stripe merchant account. If you don't have one yet, you can sign up at [stripe.com](http://stripe.com/).

---

## Step 1: **Configure Stripe OAuth and Retrievie Client ID**

1. Go to [Stripe Dashboard](https://dashboard.stripe.com/).
2. Select **Settings** in the upper right corner of the Stripe dashboard
3. Select **Connect** section  in Product settings.

    ![image.png](images/image.png)

4. Click [Onboarding options](https://dashboard.stripe.com/settings/connect/onboarding-options/countries) in **Onboard connected accounts** section

    ![image.png](images/image1.png)

5. In Oauth tab:

    ![image.png](images/image2.png)

- Enable OAuth (if it is disable)
- Add URI for the Stripe OAuth flow (e.g, https://<your-domain>/_stripe/oauth_return/)

    ![image.png](images/add-uri.png)

- Copy Client ID (Test client ID if you are in test mode)

    ![image.png](images/client-id.png)

---

## Step 2: **Retrievie Secret Key, and Publishable Key**

1. Go to [Stripe Dashboard](https://dashboard.stripe.com/).
2. Log in with your credentials.
3. In the Dashboard, navigate to:
    - Click Developers in the left menu → Click **API keys**.
4. You will see two keys:
    - **Publishable Key**: Starts with `pk_`.
    - **Secret Key**: Starts with `sk_`.

    ![image.png](images/image3.png)

5. Click **Reveal test key** or **Reveal live key** to see the **Secret Key** (depending on your mode):
    - **Test Mode**: For development and testing purposes.
    - **Live Mode**: For production use.

6. Copy both keys and store them securely.

✅ **Example:**

- **Publishable Key**: `pk_test_XXXXXXXXXXXXXXXXXXXXXXXX`
- **Secret Key**: `sk_test_XXXXXXXXXXXXXXXXXXXXXXXX`

---

## Setp 3: **Retrieve Webhook Secret Key**


1. In the Dashboard, go to:
    - Click Developers in the left menu → Click **Webhooks**.
2. Click **Add destination**

    ![image.png](images/image5.png)

3. Choose the event types:
    - Events from: Your account
    - API version: 2024-11-20.acacia
    - Events:
        - `charge.succeeded`
        - `charge.failed`
        - `charge.refunded`
        - `charge.updated`
        - `charge.dispute.created`
        - `charge.dispute.updated`
        - `charge.dispute.closed`
        - `source.chargeable`
        - `source.failed`
        - `source.canceled`
        - `payment_intent.succeeded`
        - `payment_intent.payment_failed`
        - `payment_intent.canceled`
        - `payment_intent.processing`
    - Click Continue button

    ![image.png](images/image6.png)

4. Choose Destination type:
    - Destination type: **Webhook endpoint**
    - Click Continue

    ![image.png](images/image7.png)

5. Enter the following details:

    - **Endpoint URL**: The URL in your application that will handle the webhook (e.g., `https://yourdomain.com/_stripe/webhook`).
    - **Description:** add optional description of the destination
    - Click **Create destination**

    ![image.png](images/image8.png)

6. After creating the webhook endpoint:

    ![image.png](images/image9.png)

    - Click on the endpoint you just created.

    - Click **Reveal** under **Signing secret**.

7. Copy the **Signing Secret** (starts with `whsec_`).

✅ **Example:**

- **Webhook Secret**: `whsec_XXXXXXXXXXXXXXXXXXXXXXXX`

---

## **Step 4: Add Stripe keys to Eventyay Global Settings**

1. Log in to eventyay as an admin user
2. Access to eventyay admin dashboard
3. Click to Global settings on the left menu

    ![image.png](images/global-settings.png)

4. Scoll down to Stripe settings

    ![image.png](images/image11.png)

Fill in the following fields:

- **Stripe Connect: Client ID**: [Client ID from Step 1]
- **Stripe Connect: Secret key**: [Secret key from Step 2 (live or test)]
- **Stripe Connect: Publishable key**: [Publishable key from Step 2 (live or test)]
- **Stripe Webhook: Secret key**: [Webhook secret key from Step 3]
- Click **Save**

**Note**:

1. Prerequisite is to enable Stripe payment method in at least one event to display Stripe settings on eventyay admin.
2. Some Stripe payment methods need to enable on [organizer’s Stripe account](https://dashboard.stripe.com/settings/payments) first before setting on eventyay system.
