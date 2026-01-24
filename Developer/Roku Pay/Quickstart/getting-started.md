Getting started
Integrating Roku Pay in an app is seamless. Roku Pay includes a SceneGraph ChannelStore component that contains a complete suite of APIs for managing on-device authentication, purchases, free trial offers, upgrades/downgrades, and access to content. In addition, Roku Pay includes a RESTful API and push notifications that are integrated into an app's backend system for validating, refunding, and canceling purchases.
To get started with a Roku Pay integration and test it in an app without incurring any actual charges, you first need to login to the Developer Dashboard and do the following:
Enroll in the Roku Partner Payouts Program
Specify the monetization methods for the app
Add in-app products
Create test users
Set up Roku Pay web services

Make sure you have created a Roku account and enrolled in the Roku Developer Program before completing this quickstart.
Roku Partner Payouts Program
To monetize content in an app by offering subscriptions and one-time purchases, you need to provide contact information, a payout method (direct deposit/ACH, wire transfer, or PayPal), and tax forms. See Publisher payouts for more information.
Monetization
Specify the monetization methods for your app by selecting which in-app products it will contain: in-channel subscriptions and/or in-channel one-time purchases . See Setting the monetization method for more information.
In-app products
Once your app is enabled for billing testing, you need subscription and one-time purchase products to test with. You can add one or more products to your app in a few steps. Provide basic information such as the name, unique code, and app for the product, and configure its pricing. You can also offer free trial periods and discounts for subscription products. See Adding in-app products for more information.
Test Users
Test Users can purchase in-app products on development apps without generating charges. Enter the email address of the Roku account linked to the device used for billing testing and then select the app being tested. When your testing Roku Pay in your development app, a payment method will still be required at the time of purchase; however, no charges will actually be made to the test user's method of payment. See Creating test users for more information.
Roku Pay web services
Roku Pay includes web services that developers can integrate into their publisher's backend system for validating, refunding, and canceling transactions related to subscriptions and one-time purchases. Validating transactions is especially critical because it enables apps to check whether customers are entitled to content. The Roku Pay web services make this easy by returning a single isEntitled flag that indicates whether to grant access. In addition to pulling transactions via the Roku Pay web services, publishers can receive metadata about the transactions in near real-time via push notifications. See Setting up Roku Pay web services to get your Roku Pay API Key and provide a push notification URL.