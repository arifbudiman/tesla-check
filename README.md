# Tesla: Estimated Delivery Date Checker

Checks the estimated delivery date for your Tesla order.

## Getting Started

After cloning the repo, create an environment variable file `.env` with a restrictive file permissions for the following variables:
<pre>
EMAIL="your-email-address"
CREDENTIAL="your-tesla-account-credential"
REFERENCE_NUMBER="your-tesla-reservation-number"
USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
LOGIN_FORM_URL="https://auth.tesla.com/oauth2/v1/authorize?redirect_uri=https://www.tesla.com/teslaaccount/owner-xp/auth/callback&response_type=code&client_id=ownership&scope=openid%20email&audience=https%3A%2F%2Fownership.tesla.com%2F"
MANAGE_URL="https://www.tesla.com/teslaaccount/profile?rn="
EMAIL_RESULT="False"
</pre>

* EMAIL: the email address you use to login to your Tesla account.
* CREDENTIAL: the password of your Tesla account.
* REFERENCE_NUMBER: your Tesla order reservation number, usually starts with "RN".
* EMAIL_RESULT: set to "False" to print the result, or "True" to email you the result.

## Requirements

* [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)

## Usage

`python ./check-edd.py `

To check periodically, you can schedule (e.g. via cron) the script to run at a fixed interval (e.g. daily) and email you the result.
