import json

import iyzipay

options = {
    'api_key': "sandbox-odVGhnYPNFNW4yJday7u5KcdWIdB03lI",
    'secret_key': "sandbox-0CDV337XXxEgGq8RpOYp0TxF9FxKuKeF",
    'base_url': "sandbox-api.iyzipay.com"
}

buyer = {
    'id': 'BY789',
    'name': 'John',
    'surname': 'Doe',
    # 'gsmNumber': '+905350000000',
    'email': 'email@email.com',
    'identityNumber': '74300864791',
    # 'lastLoginDate': '2015-10-05 12:43:35',
    # 'registrationDate': '2013-04-21 15:12:09',
    'registrationAddress': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
    'ip': '85.34.78.112',
    'city': 'Istanbul',
    'country': 'Turkey'
    # 'zipCode': '34732'
}

buyer = {
    'id': '1',
    'name': 's', 'surname': 's', 'email': 'admin@printerush.com', 'identityNumber': '74300864791', 'ip': '85.34.78.112', 'gsmNumber': 'd', 'city': 'İzmir', 'country': 'Türkiye', 'registrationAddress': 'd'}
address = {
    'contactName': 'Jane Doe',
    'city': 'Istanbul',
    'country': 'Turkey',
    'address': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1'
    # 'zipCode': '34732'
}

basket_items = [
    {
        'id': 'BI101',
        'name': 'Binocular',
        'category1': 'Collectibles',
        'category2': 'Accessories',
        'itemType': 'PHYSICAL',
        'price': '0.3'
    },
    {
        'id': 'BI102',
        'name': 'Game code',
        'category1': 'Game',
        'category2': 'Online Game Items',
        'itemType': 'VIRTUAL',
        'price': '0.5'
    },
    {
        'id': 'BI103',
        'name': 'Usb',
        'category1': 'Electronics',
        'category2': 'Usb / Cable',
        'itemType': 'PHYSICAL',
        'price': '0.2'
    }
]
basket_items = [{'id': 1, 'name': 'Ürün 1', 'category1': 'Masa Lambası', 'itemType': 'PHYSICAL', 'price': 10.5}, {'id': 1, 'name': 'Ürün 1', 'category1': 'Masa Lambası', 'itemType': 'PHYSICAL', 'price': 10.5}, {'id': 1, 'name': 'Ürün 1', 'category1': 'Masa Lambası', 'itemType': 'PHYSICAL', 'price': 10.5}, {'id': 1, 'name': 'Ürün 1', 'category1': 'Masa Lambası', 'itemType': 'PHYSICAL', 'price': 10.5}, {'id': 1, 'name': 'Ürün 1', 'category1': 'Masa Lambası', 'itemType': 'PHYSICAL', 'price': 10.5}, {'id': 2, 'name': 'Ürün 2', 'category1': 'Tavan Lambası', 'itemType': 'PHYSICAL', 'price': 100.0}]

request = {
    'locale': 'tr',
    # 'conversationId': '123456789',
    'price': '152.5',
    'paidPrice': '1',
    'currency': 'TRY',
    # 'basketId': 'B67832',
    # 'paymentGroup': 'PRODUCT',
    "callbackUrl": "https://www.merchant.com/callback",
    "enabledInstallments": ['2', '3', '6', '9'],
    'buyer': buyer,
    'shippingAddress': address,
    'billingAddress': address,
    'basketItems': basket_items
}


# request = {
#     'locale': 'tr',
#     'price': 152.5,
#     'paidPrice': 152.5,
#     'currency': 'TRY',
#     'callbackUrl': 'https://www.merchant.com/callback',
#     'enabledInstallments': ['2', '3', '6', '9'],
#     'buyer': buyer, 'shippingAddress': {'contactName': 'd d', 'city': 'İzmir', 'country': 'Türkiye', 'address': 'd'}, 'billingAddress': {'contactName': 'd d', 'city': 'İzmir', 'country': 'Türkiye', 'address': 'd'}, 'basketItems': [{'id': 1, 'name': 'Ürün 1', 'category1': 'Masa Lambası', 'itemType': 'PHYSICAL', 'price': 10.5}, {'id': 1, 'name': 'Ürün 1', 'category1': 'Masa Lambası', 'itemType': 'PHYSICAL', 'price': 10.5}, {'id': 1, 'name': 'Ürün 1', 'category1': 'Masa Lambası', 'itemType': 'PHYSICAL', 'price': 10.5}, {'id': 1, 'name': 'Ürün 1', 'category1': 'Masa Lambası', 'itemType': 'PHYSICAL', 'price': 10.5}, {'id': 1, 'name': 'Ürün 1', 'category1': 'Masa Lambası', 'itemType': 'PHYSICAL', 'price': 10.5}, {'id': 2, 'name': 'Ürün 2', 'category1': 'Tavan Lambası', 'itemType': 'PHYSICAL', 'price': 100.0}]}

checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(request, options)
s = """{"status":"success","locale":"tr","systemTime":1593038749708,"token":"2d0cf393-bb9b-40b1-9d59-e8bfc363dfc5","checkoutFormContent":"<script type=\"text/javascript\">if (typeof iyziInit == 'undefined') {var iyziInit = {currency:\"TRY\",token:\"2d0cf393-bb9b-40b1-9d59-e8bfc363dfc5\",price:1.00,locale:\"tr\",baseUrl:\"https://sandbox-api.iyzipay.com\", merchantGatewayBaseUrl:\"https://sandbox-merchantgw.iyzipay.com\", registerCardEnabled:true,bkmEnabled:true,bankTransferEnabled:false,bankTransferRedirectUrl:\"https://www.merchant.com/callback\",bankTransferCustomUIProps:{},creditCardEnabled:true,bankTransferAccounts:[],userCards:[],fundEnabled:true,memberCheckoutOtpData:{},force3Ds:false,isSandbox:true,storeNewCardEnabled:true,paymentWithNewCardEnabled:true,enabledApmTypes:[\"SOFORT\",\"IDEAL\",\"QIWI\",\"GIROPAY\"],payWithIyzicoUsed:false,payWithIyzicoEnabled:true,payWithIyzicoCustomUI:{},buyerName:\"s\",buyerSurname:\"s\",merchantInfo:\"\",buyerProtectionEnabled:false,hide3DS:false,gsmNumber:\"\",email:\"admin@printerush.com\",checkConsumerDetail:{},subscriptionPaymentEnabled:false,ucsEnabled:false,metadata : {},createTag:function(){var iyziJSTag = document.createElement('script');iyziJSTag.setAttribute('src','https://sandbox-static.iyzipay.com/checkoutform/v2/bundle.js?v=1593038749703');document.head.appendChild(iyziJSTag);}};iyziInit.createTag();}</script>","tokenExpireTime":1800,"paymentPageUrl":"https://sandbox-cpp.iyzipay.com?token=2d0cf393-bb9b-40b1-9d59-e8bfc363dfc5&lang=tr"}"""
# json.loads(checkout_form_initialize.read().decode('utf-8'))
print(checkout_form_initialize.read().decode('utf-8'))
print(checkout_form_initialize.read().decode('utf-8'))

