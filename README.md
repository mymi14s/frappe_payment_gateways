
  

## Frappe Payment Gateways

  

Frappe/ERPNext payment gateways for Paystack, Flutter, Okra and Many more.

Currently, Paystack is supported for payment collection, supported paystack currency [USD, NGN, ZAR, GHS].

  

Payment made will be logged to ***Payment Gateway Log*** doctype

  

**TODO**

  

- Auto Create payment entry

- Auto link customer email in Payment Gateway Request

- Payment Request email formatting with links

- Flutter and Okra gateway

  

**NOTE**

Do not use in production as we are currently testing the app. use only test keys for the now.

  

**PAYSTACK**

webhook url: https://your-urls.com/api/method/frappe_payment_gateways.www.payment.pay.index.webhook

![image](https://github.com/mymi14s/frappe_payment_gateways/assets/10146518/fe42be5f-b262-438d-b97a-d9ae5641cabc)

  
  

#### License

  

MIT

  

## SETUP
bench get-app --branch=master https://github.com/mymi14s/frappe_payment_gateways
bench --site sitename install-app frappe_payment_gateways
bench --site sitename migrate


- Add Paystack Key and check enabled.

![image](https://github.com/mymi14s/frappe_payment_gateways/assets/10146518/c51e02fb-ed68-4805-8597-f0623d66e042)

- In Sales Invoice

![image](https://github.com/mymi14s/frappe_payment_gateways/assets/10146518/4e68793d-a163-444a-ad7d-dcbf61df98d3)

- Add customer email address

![image](https://github.com/mymi14s/frappe_payment_gateways/assets/10146518/ea3947d7-7342-4a07-9fd9-f79339fdc116)

![image](https://github.com/mymi14s/frappe_payment_gateways/assets/10146518/5fbbb28d-afbe-46a5-834e-790c5a452b4e)

- Payment link will be sent to the email, visit the email to make payment

![image](https://github.com/mymi14s/frappe_payment_gateways/assets/10146518/dd95a001-45f4-498a-b2e0-2d604981b997)

![image](https://github.com/mymi14s/frappe_payment_gateways/assets/10146518/84fc6622-4b33-4db5-ade1-602183184aec)