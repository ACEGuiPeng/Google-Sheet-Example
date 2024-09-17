# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : test.py
@Author: White Gui
@Date  : 2024/9/17
@Desc :
"""
import unittest

from dotenv import load_dotenv

from service.google_auth import access_token_from_impersonated_credentials


class TestTemplate(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_access_token_from_impersonated_credentials(self):
        load_dotenv()
        impersonated_service_account = "google-sheet-app@lateral-origin-435912-f8.iam.gserviceaccount.com"
        scopes = ['https://www.googleapis.com/auth/cloud-platform',
                  'https://www.googleapis.com/auth/spreadsheets.readonly',
                  'https://www.googleapis.com/auth/drive']
        target_credentials = access_token_from_impersonated_credentials(impersonated_service_account, scopes)
        self.assertIsNotNone(target_credentials)


if __name__ == '__main__':
    unittest.main()
