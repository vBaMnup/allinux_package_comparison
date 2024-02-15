from .altapi import AltApi as AltLinuxAPI
import asyncio
import json
import sys


async def compare_packages(branch1, branch2):
    api = AltLinuxAPI()
    packages_branch1 = await api.get_branch_binary_packages(branch1)
    packages_branch2 = await api.get_branch_binary_packages(branch2)
    missing_in_branch1 = [
        pkg for pkg in packages_branch2 if pkg not in packages_branch1
    ]
    missing_in_branch2 = [
        pkg for pkg in packages_branch1 if pkg not in packages_branch2
    ]

    higher_version_in_branch1 = []
    for pkg1 in packages_branch1:
        for pkg2 in packages_branch2:
            if (
                pkg1["name"] == pkg2["name"]
                and pkg1["version-release"] > pkg2["version-release"]
            ):
                higher_version_in_branch1.append(pkg1)

    return {
        "missing_in_branch1": missing_in_branch1,
        "missing_in_branch2": missing_in_branch2,
        "higher_version_in_branch1": higher_version_in_branch1,
    }


async def main():
    if len(sys.argv) != 3:
        print("Usage: python compare_packages.py <branch1> <branch2>")
        sys.exit(1)

    branch1 = sys.argv[1]
    branch2 = sys.argv[2]

    result = await compare_packages(branch1, branch2)
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    asyncio.run(main())
