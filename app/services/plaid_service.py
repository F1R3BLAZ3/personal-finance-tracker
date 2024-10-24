import os
from flask import current_app
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest, LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.errors import ApiException
from werkzeug.exceptions import InternalServerError

def get_plaid_client():
    configuration = plaid_api.Configuration(
        host=current_app.config['PLAID_ENV'],
        api_key={
            'clientId': current_app.config['PLAID_CLIENT_ID'],
            'secret': current_app.config['PLAID_SECRET'],
        }
    )
    return plaid_api.PlaidApi(configuration)

def create_link_token(user_id):
    client = get_plaid_client()
    request = LinkTokenCreateRequest(
        user=LinkTokenCreateRequestUser(client_user_id=user_id),
        client_name="Your App Name",
        products=[Products('transactions')],
        country_codes=[CountryCode('US')],
        language='en'
    )
    try:
        response = client.link_token_create(request)
        return response['link_token']
    except ApiException as e:
        current_app.logger.error(f"Error creating link token: {e}")
        raise InternalServerError('Unable to create link token')

def exchange_public_token(public_token):
    client = get_plaid_client()
    request = ItemPublicTokenExchangeRequest(public_token=public_token)
    try:
        response = client.item_public_token_exchange(request)
        return response['access_token']
    except ApiException as e:
        current_app.logger.error(f"Error exchanging public token: {e}")
        raise InternalServerError('Unable to exchange public token')

def get_transactions(access_token, start_date, end_date):
    client = get_plaid_client()
    request = TransactionsGetRequest(
        access_token=access_token,
        start_date=start_date,
        end_date=end_date
    )
    try:
        response = client.transactions_get(request)
        return response['transactions']
    except ApiException as e:
        current_app.logger.error(f"Error fetching transactions: {e}")
        return []
