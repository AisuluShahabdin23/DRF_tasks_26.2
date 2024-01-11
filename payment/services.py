import stripe
from payment.models import Payment


def get_pay(amount_payment, user):
    stripe.api_key = 'sk_test_51OXPo8I8CHYfroxkLtwikhg0KmhLRUJ7pZvrvrhP5nLm213M1dfv5hvgvKgUETj6JojpsYBlFmjCa7OvwxMUCwu300Gd7TpoQa'
    pay = stripe.PaymentIntent.create(
        amount=amount_payment,
        currency="usd",
        automatic_payment_methods={"enabled": True}
    )

    payment = Payment.objects.create(
        user=user,
        amount_payment=amount_payment,
        stripe_id=pay.id
    )

    return payment
