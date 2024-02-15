import aiohttp


class AltLinuxAPI:
    """AltApi class"""

    def __init__(self, session: aiohttp.ClientSession):
        """
        Initialize AltApi class
        """
        self.base_url = "https://rdb.altlinux.org/api/"

    async def get_branch_binary_packages(self, branch):
        """
        Get branch binary packages
        """
        url = f"{self.base_url}/export/branch_binary_packages/{branch}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()
