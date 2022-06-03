import mercadopago
import json

CLIENT_ID = '5917159165109980'
CLIENT_SECRET = 'kCcajl6ophFEDYDx1RdGGTwsQGqBUm2H'


def payment(req, **kwargs):
    product = kwargs['product']
    preference = {
      "items": [
        {
          "title": product.name,
          "quantity": product.quantity,
          "currency_id": "BRL",
          "unit_price": product.price
        }
      ]
    }

    mp = mercadopago.MP(CLIENT_ID, CLIENT_SECRET)

    preferenceResult = mp.create_preference(preference)

    url = preferenceResult["response"]["init_point"]
    
    return url
