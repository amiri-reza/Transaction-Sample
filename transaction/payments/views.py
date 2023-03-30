from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
import stripe
from users.models import User


class PaymentView(TemplateView):
    template_name = "payments/home.html"
    # form_class = PaymentForm
    # success_url = 'success'


@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {"publicKey": settings.STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == "GET":
        domain_url = "http://localhost:8000/"
        stripe.api_key = settings.STRIPE_API_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id
                if request.user.is_authenticated
                else None,
                success_url=domain_url
                + "payments/"
                + "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "payments/" + "cancelled/",
                payment_method_types=["card"],
                mode="payment",
                line_items=[
                    {
                        "price": "price_1Mj92lGnzEzb9V8cSc17vsVM",
                        "quantity": 1,
                    }
                ],
            )

            print("------------------", request.user.id)
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})


class SuccessView(TemplateView):
    template_name = "payments/success.html"


class CancelledView(TemplateView):
    template_name = "payments/cancelled.html"


@csrf_exempt
def stripe_webhook(request):
    print("------------------------------------------", request)
    stripe.api_key = settings.STRIPE_API_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        # breakpoint()
        # form = PaymentForm(request.POST)
        # if form.is_valid():    #  and request.user.is_authenticated()
        #     amount = form.amount
        user_id = event.data.object.client_reference_id
        user = User.objects.get(id=user_id)
        user.usercoins.coins = user.usercoins.coins + 1
        user.usercoins.save()
        print("Payment was successful.")
        # else:
        #     return PaymentForm()
    return HttpResponse(status=200)

