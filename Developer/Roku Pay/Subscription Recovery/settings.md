Subscription Recovery settings
You can use the Subscription recovery page in the Developer Dashboard to enable Enhanced Subscription Recovery for your apps. The page lists the subscription recovery solution ( basic or enhanced ) used for each public and beta app in your developer account and lets you enable the enhanced recovery solution.
Read the Enhanced Subscription Recovery documentation before enabling this feature for your apps. This integration requires you to update entitlements in your system based on the Roku Pay transaction data you pull from the Roku Pay web services and/or receive via push notifications .
If this feature is not implemented correctly, customers will be unable to purchase a subscription for your app until the on-hold period has elapsed.
Enabling Enhanced Subscription Recovery
To enable the enhanced recovery solution for a public or beta app, follow these steps:
Verify that you have completed the Enhanced Subscription Recovery integration and published the updated version of your app .
Under Monetization in the left sidebar, click Subscription Recovery .
Click the Edit icon on the right-hand side of the app.
In the Subscription recovery settings dialog, click Enhanced and then click Continue .
Click Yes, Enable . Once you switch a app to enhanced subscription recovery, you can cannot switch it back to basic recovery.

Configuring the grace period
Once enhanced subscription recovery is enabled for an app, you can configure the grace period. By default, apps use a 3-day grace period in which Roku notifies customers daily via email to update their method of payment (MOP). You can switch the grace period to 0, 10, 11, 13, or 16 days). Once grace period expires, the subscription is placed on hold. Selecting a 0-day grace period means that a customer's subscription is placed directly on hold if their payment renewal fails.
To change the grace period, follow these steps:
Click the Edit icon on the right-hand side of the app.
Under Select a grace period , select the duration you want to use for your app: 0 , 3 default), 10 , 11 , 13 , or 16 days.
Click Save .

Switching subscription recovery settings
Once enhanced subscription recovery is enabled, it is used from that point forward for all subscriptions coming up for renewal. Basic recovery is still used for subscriptions currently in a grace period. Once you switch a app to enhanced subscription recovery, you can cannot switch it back to basic recovery.