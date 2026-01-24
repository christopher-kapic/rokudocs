Testing a Roku Pay app
Testing the purchase and entitlement workflows in your Roku Pay workflow entails three major steps:
Verifying that content cannot be accessed without a subscription.
A subscription can be purchased.
Access to content is granted with a valid subscription.

These steps are based on the Roku Pay workflows specified in the On-device authentication guide .
Before running any Roku Pay tests on an app, make sure to add one or more in-app products to the app, enable the app for billing testing, add yourself as a Test User to the app, and then sideload the app .
In-app products : Developers must add one or more in-app products to the app being tested. If the app has one or more sets of mutually exclusive products, create product groups for each set. To test entitlements after a free trial expires, create a product that includes a 1-day free trial .
Billing Testing : Developers can designate an app for "billing testing" to observe output from the SceneGraph ChannelStore node in the debug console when the app is sideloaded. The billing testing feature provides developers with visibility into the confirmations, error codes, and other transactional metadata related to purchases made with Roku Pay.
Test Users . Developers can add themselves as a Test User to the app being tested in order to execute ChannelStore purchases without being billed for the transactions.

Verifying no entitlement without a Roku Pay subscription
To verify that a customer cannot be entitled to content without a subscription purchased through Roku Pay, follow these steps:
Launch app and select content behind paywall.

Send the getAllPurchases command . Verify that it does not return any active subscription products.

Call the roRegistrySection.read() function on the device registry section for the app. Verify that it does not return an access token from device registry.

Send the getChannelCred command . Verify that it does not return an access token from Roku cloud.

Verifying Roku Pay purchase workflow
To verify that a customer can purchase a subscription product and upgrade/downgrade their plan through Roku Pay, follow these steps:
Send the getCatalog command . Verify that the SceneGraph components used to display in-app products are populated with product metadata.

Select a subscription product. Verify that the getUserData command is sent and the request for information (RFI) screen is displayed.

Press Continue on the RFI screen. Verify that the order is created and the doOrder command is executed.

Verify that the order confirmation screen displays any free trial offers or discounts included with the subscription product.

Confirm the order of the subscription product. Verify that the orderStatus field confirms that the order was successfully completed.

Verify that an access token is generated in the publisher's backend system and passed into: a. The storeChannelCredData command to store the access token in the Roku cloud. b. The roRegistrySection.write() function to store the access token in the device registry.
If your app includes a product group , select another in-app product that is in the same product group as the previously ordered one. Verify that the "You're already subscribed" dialog is displayed.

Call the validate-transaction API with purchase ID included in the orderStatus field. Verify that the isEntitled flag is set to "true".

If your app includes multiple subscription plans, upgrade or downgrade the subscription plan, and then do the following: a. Verify that the order.action field is set to the correct string. b. Call the validate-transaction API with purchase ID included in the orderStatus field. Confirm the following: The purchase_type is set to UPGRADE or DOWNGRADE . The cancelled_transaction_ids field is set to the transaction ID of the original subscription purchase. The purchase_status field is set to active .

Close the app.

Verifying Roku Pay entitlement workflow
To verify that a customer is entitled to content after purchasing a subscription through Roku Pay, follow these steps:
Re-launch app.

Send the getAllPurchases command . Verify that it returns the purchased subscription product.

Call the validate-transaction API with purchase ID included in the purchases field. Verify that the isEntitled flag is set to "true".

Call the roRegistrySection.read() function on the device registry section for the app. Verify that it returns an access token from the device registry.

Send the getChannelCred command . Verify that it returns an access token from Roku cloud.

To test that customers are not entitled to subscription products after a free trial ends, do the following: a. Order a subscription product that has a 1-day free trial. b. After the trial expires the next day, cancel the subscription. c. Complete steps 1-3. Verify that the isEntitled flag is set to "false".