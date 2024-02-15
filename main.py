from urllib import request, error
import json
import argparse
import sys


def get_packages(branch, arch):
    url = f"https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}"

    if arch:
        url += f"?arch={arch}"

    try:
        with request.urlopen(url) as response:
            if response.status == 200:
                data = json.loads(response.read())
                return data["packages"]
            else:
                print(f"Ошибка при получении данных из REST API: {response.status}")
                sys.exit(1)
    except error.URLError as e:
        print(f"Ошибка при обращении к REST API: {e.reason}")
        sys.exit(1)


def compare_packages(packages1, packages2):
    packages_dict1 = {p["name"]: (p["version"], p["release"]) for p in packages1}
    packages_dict2 = {p["name"]: (p["version"], p["release"]) for p in packages2}
    missing_in_1 = []
    missing_in_2 = []
    newer_in_1 = []

    for name, vr in packages_dict1.items():
        if name not in packages_dict2:
            missing_in_2.append(name)
        else:
            vr2 = packages_dict2[name]
            if vr > vr2:
                newer_in_1.append(name)

    for name in packages_dict2.keys():
        if name not in packages_dict1:
            missing_in_1.append(name)

    return missing_in_1, missing_in_2, newer_in_1


def format_result(missing_in_1, missing_in_2, newer_in_1):
    result = {
        "packages_in_p10_but_not_in_sisyphus": missing_in_1,
        "packages_in_sisyphus_but_not_in_p10": missing_in_2,
        "packages_with_higher_version_release_in_sisyphus": newer_in_1,
    }
    result_json = json.dumps(result, indent=4)
    return result_json


parser = argparse.ArgumentParser(
    description="Сравнивает бинарные пакеты веток sisyphus и p10 из REST API базы данных ALT Linux"
)
parser.add_argument(
    "-a",
    "--arch",
    choices=["aarch64", "armh", "i586", "noarch", "ppc64le", "x86_64"],
    help="Архитектура пакетов",
)
parser.add_argument(
    "-o", "--output", help="Имя файла для сохранения результата в формате JSON"
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
    print(f"Результат сравнения сохранен в файл {args.output}")
else:
    print(result_json)
