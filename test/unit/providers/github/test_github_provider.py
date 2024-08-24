# import pytest
# from unittest.mock import Mock
# from requests import get
# import os
# import sys

# dir = os.path.dirname(__file__)
# sys.path.append(os.path.join(dir, "..", "..", "..", "..", "explain_pr"))

# from providers.github.github_provider import GitHubProvider


# # def setup_function():
# #     pass

# # def teardown_function():
# #     pass


# def mock_requests_get():
#     mock_get = Mock(spec=get)

#     mock_get.url = "https://api.github.com/repos/owner/repository/pulls/1"
#     mock_get.headers = {}
#     mock_get.timeout = 0
#     data = {"title": "title", "body": "description"}
#     mock_get.json.return_value = (
#         f'{{"title": "{data["title"]}", "body": "{data["body"]}"}}'
#     )

#     return mock_get


# def test_get_pr_details_with_valid_pr_number(mock_requests_get):
#     # Arrange
#     git_provider = GitHubProvider()

#     # Act
#     response_title, response_body = git_provider._get_pr_details(
#         "owner", "repository", 1
#     )

#     # Assert
#     assert response_title == mock_requests_get.json()["title"]
#     assert response_body == mock_requests_get.json()["body"]
#     mock_requests_get.assert_called_once_with(
#         "https://api.github.com/repos/owner/repository/pulls/1",
#         headers=mock_requests_get.headers,
#         timeout=mock_requests_get.timeout,
#     )
