# Honulabs CLI
A simple and easy to use CLI for interaction with the Honulabs API to generate and deploy micro-saas businesses

# Requirements
- Python 3.11 or higher
- Poetry

## External Requirements
- A Google Analytics account with the display name `HonuLabs`
- A Google Ads account
- A Sendgrid account
- A Google Tag Manager account

The following services should then be connected on your HAP account;
- GoogleTagManagerService
- SendgridService
- StripeService
- GoogleAnalyticsAdminService
- GoogleAdsService
- GoogleAnalyticsService

# Usage
1. Clone the repo to your local machine.
2. Run `poetry install` to install packages.
3. Run `poetry run python -m cli` to run the cli.
4. Log in with the `login` command using a Honu Agent Platform token.
