from django.http import HttpResponse

class StripeWH_Handler:
    """ handle stipe webhooks """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """ handle webhook event """

        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """ handle webhook event: succeedd payment """

        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.data.charges[0].amount / 100, 2)

        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        order_exists = False
        try:
            order = Order.objects.get(
                full_name__iexact=shipping_details.name,
                email__iexact=shipping_details.email,
                phone_number__iexact=shipping_details.phone,
                country__iexact=shipping_details.country,
                postcode__iexact=shipping_details.postal_code,
                town_or_city__iexact=shipping_details.city,
                street_address1__iexact=shipping_details.line1,
                street_address2__iexact=shipping_details.line2,
                county__iexact=shipping_details.state,
                grand_total=grand_total,
            )
            order_exists = True
            return HttpResponse(
                content=f'Webhook received: {event["type"]}',
                status=200)
        except Order.DoesNotExist:

            
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """ handle webhook event: failed payment """

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
