Creating test users
Test users can make in-app purchases free-of-charge for testing purposes. This is useful for testing the Roku Pay integration in an app.
In order for a test user to make free in-app purchases on an app:
The test user must be associated with the app being tested.
The test user's Roku account must be linked to the Roku device on which the app is installed.

Adding a test user
To create a test user and add apps to it, follow these steps:
In the Developer Dashboard , select Test Users under Monetization .

The Manage test users index page lists the email addresses and apps for each test user. Click Add New Test User .

In the Test User Email box, enter the email address of the test user. The test user must be the app's root account user .

From the Channels list, select one or more apps on which the test user can make free purchases.

Click Add . The test user is listed in the Manage test users index page.

To edit the email address or apps of the test user, click Edit , make changes, and then click Update .

Viewing and voiding transactions
You can view all the transactions made by test users on your apps. You can also void all the transactions made by the test user on a specific to re-test the purchase workflows on that app with that test user. To view and void the transactions of a test user, follow these steps:
Under the Transactions column in the test user's row, click View .

The Test user transaction page lists each transaction made by the test user per app, including the purchase date, app name, transaction ID (used by the Roku Pay Web Service API for validating, refunding, and canceling purchases), and product name.

To void the transactions made by the test user on a specific app, click Void transactions . All transactions made by the test user on that app are permanently deleted. The transaction IDs of the voided transactions are not accessible via the Roku Pay Web Service API.