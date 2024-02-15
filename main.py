#!/usr/bin/python3

import argparse
import json
from urllib import request, error


def get_packages(branch, arch):
    """
    Get packages from REST API
    """
    url_template = "https://rdb.altlinux.org/api/export/branch_binary_packages/{}"
    url = url_template.format(branch)

    if arch:
        url += "?arch={}".format(arch)

    try:
        response = request.urlopen(url)
        if response.status == 200:
            data = json.loads(response.read().decode("utf-8"))
            return data["packages"]
        else:
            raise RuntimeError(
                f"Error getting packages from REST API: {response.status}"
            )
    except error.URLError as e:
        raise RuntimeError(f"Error when accessing REST API: {e.reason}")


def compare_packages(packages1, packages2):
    """
    Compare packages from two branches
    """
    packages_dict1 = {p["name"]: (p["version"], p["release"]) for p in packages1}
    packages_dict2 = {p["name"]: (p["version"], p["release"]) for p in packages2}
    missing_in_1 = set(packages_dict2.keys()) - set(packages_dict1.keys())
    missing_in_2 = set(packages_dict1.keys()) - set(packages_dict2.keys())
    newer_in_1 = [
        name
        for name in packages_dict1
        if name in packages_dict2 and packages_dict1[name] > packages_dict2[name]
    ]
    return list(missing_in_1), list(missing_in_2), newer_in_1


def format_result(missing_in_1, missing_in_2, newer_in_1):
    """
    Format the result
    """
    result = {
        "packages_in_p10_but_not_in_sisyphus": missing_in_1,
        "packages_in_sisyphus_but_not_in_p10": missing_in_2,
        "packages_with_higher_version_release_in_sisyphus": newer_in_1,
    }

    return json.dumps(result, indent=4)


parser = argparse.ArgumentParser(
    description="Compares sisyphus and p10 branch binary packages from ALT Linux database REST APIs"
)
parser.add_argument(
    "-a",
    "--arch",
    choices=["aarch64", "armh", "i586", "noarch", "ppc64le", "x86_64"],
    help="Package Architecture",
)
parser.add_argument(
    "-o", "--output", help="File name for saving the result in JSON format"
)
args = parser.parse_args()

packages_sisyphus = get_packages("sisyphus", args.arch)
packages_p10 = get_packages("p10", args.arch)
missing_in_p10, missing_in_sisyphus, newer_in_sisyphus = compare_packages(
    packages_sisyphus, packages_p10
)
result_json = format_result(missing_in_p10, missing_in_sisyphus, newer_in_sisyphus)

if args.output:
    with open(args.output, "w") as f:
        f.write(result_json)
    print(f"The result of the comparison is saved to a file {args.output}")
else:
    print(result_json)
