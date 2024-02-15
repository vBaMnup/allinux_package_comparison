# AlT API linux Package comparison utility
This utility is for comparing sisyphus and p10 branch packages

## How to use:

### Download main.py

1. Download [script file](https://github.com/vBaMnup/allinux_package_comparison/releases/download/v0.1-beta/compare_packege) from repository
2. Navigate to the directory of the downloaded file
3. Make the script executable by using the 
```shell
chmod +x compare_packages
```
3. Выполните команду:
```shell
./compare_packages
```
### Note
To filter by arch, use the -a -arch argument
```shell
./compare_packages --arch x86_64
```

To save the result to a file, use the argument "-o", "--output" 
```shell
./compare_packege -o result.json
```
