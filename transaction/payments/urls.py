from django.urls import path, include
from payments import views


# app_name = "payments"
urlpatterns = [
    path("", views.PaymentView.as_view(), name="home"),
    path("config/", views.stripe_config),
    path("create-checkout-session/", views.create_checkout_session),
    path("success/", views.SuccessView.as_view()),
    path("cancelled/", views.CancelledView.as_view()),
    path("webhook/", views.stripe_webhook),
    

]
