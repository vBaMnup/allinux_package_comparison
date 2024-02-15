import unittest
from unittest.mock import Mock, patch
from src.altapi import AltApi


class TestAltApi(unittest.TestCase):
    """ Test case for AltApi """
    def setUp(self):
        self.session = Mock()

    @patch("aiohttp.ClientSession.get")
    async def test_get_branch_binary_packages_positive(self, mock_get):
        """ Test case for get_branch_binary_packages """
        mock_response = Mock()
        mock_response.json = Mock(return_value={"packages": ["package1", "package2"]})
        mock_get.return_value = mock_response

        alt_api = AltApi(self.session)
        result = await alt_api.get_branch_binary_packages("branch")

        self.assertEqual(result, {"packages": ["package1", "package2"]})

    @patch("aiohttp.ClientSession.get")
    async def test_get_branch_binary_packages_negative(self, mock_get):
        """ Test case for get_branch_binary_packages """
        mock_response = Mock()
        mock_response.json = Mock(return_value={})
        mock_get.return_value = mock_response

        alt_api = AltApi(self.session)
        result = await alt_api.get_branch_binary_packages("branch")

        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
