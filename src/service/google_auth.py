# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : google_auth.py
@Author: White Gui
@Date  : 2024/9/17
@Desc :
"""
import os

import google.auth
import google.auth.transport.requests
from google.auth import impersonated_credentials
from google.oauth2.service_account import Credentials


def access_token_from_impersonated_credentials(
        impersonated_service_account: str, scopes: list
):
    """
      Use a service account (SA1) to impersonate another service account (SA2)
      and obtain an ID token for the impersonated account.
      To obtain a token for SA2, SA1 should have the
      "roles/iam.serviceAccountTokenCreator" permission on SA2.

    Args:
        impersonated_service_account: The name of the privilege-bearing service account for whom the credential is created.
            Examples: name@project.service.gserviceaccount.com

        scopes: Provide the scopes that you might need to request to access Google APIs,
            depending on the level of access you need.
            For this example, we use the cloud-wide scope and use IAM to narrow the permissions.
            https://cloud.google.com/docs/authentication#authorization_for_services
            For more information, see: https://developers.google.com/identity/protocols/oauth2/scopes
    """

    # Construct the GoogleCredentials object which obtains the default configuration from your
    # working environment.
    credentials_dict = {
        'type': 'service_account',
        "project_id": os.getenv('PROJECT_ID'),
        "private_key_id": os.getenv('PRIVATE_KEY_ID'),
        "private_key": os.getenv('PRIVATE_KEY').replace('\\n', '\n'),
        "client_email": os.getenv('CLIENT_EMAIL'),
        "client_id": os.getenv('CLIENT_ID'),
        "auth_uri": os.getenv('AUTH_URI'),
        "token_uri": os.getenv('TOKEN_URI'),
        "auth_provider_x509_cert_url": os.getenv('AUTH_PROVIDER_X509_CERT_URL'),
        "client_x509_cert_url": os.getenv('CLIENT_X509_CERT_URL'),
        "universe_domain": os.getenv('UNIVERSE_DOMAIN')
    }

    credentials = Credentials.from_service_account_info(credentials_dict,
                                                        scopes=scopes)

    # Create the impersonated credential.
    target_credentials = impersonated_credentials.Credentials(
        source_credentials=credentials,
        target_principal=impersonated_service_account,
        # delegates: The chained list of delegates required to grant the final accessToken.
        # For more information, see:
        # https://cloud.google.com/iam/docs/create-short-lived-credentials-direct#sa-credentials-permissions
        # Delegate is NOT USED here.
        delegates=[],
        target_scopes=scopes,
        lifetime=300,
    )

    # Get the OAuth2 token.
    # Once you've obtained the OAuth2 token, use it to make an authenticated call
    # to the target audience.
    request = google.auth.transport.requests.Request()
    target_credentials.refresh(request)
    # The token field is target_credentials.token.
    return target_credentials
