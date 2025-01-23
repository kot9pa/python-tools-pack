import argparse
from itertools import groupby
from shutil import rmtree
from tqdm import tqdm
from os import walk, remove, path
from re import match, search

''' 
Script for recursive delete specified path
usage: 2_rmpath_tool.py [-h] path

positional arguments:
  path        path, e.g. 'path\\to\\delete'

options:
  -h, --help  show this help message and exit
'''

result = dict()
regex = rf'\..+$'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help=r"path, e.g. 'path\to\delete'")
    args = vars(ap.parse_args())

    # bug https://github.com/python/cpython/issues/122919
    path_to_delete = args['path'].rstrip('"')
    if not path.exists(path_to_delete):
        raise FileNotFoundError(f"{path_to_delete=} was not found")

    for root, dirs, files in walk(path_to_delete):
        print(f"'{root}' have {len(files)} files and {len(dirs)} dirs")
        result['dir'] = result.get('dir', 0) + len(dirs)
        for ext, files in groupby(sorted(map(lambda f: f.split(".")[-1]
                                             if search(regex, f) else 'no_ext', files))):
            result[ext] = result.get(ext, 0) + len(list(files))

    confirm = input(f"\nDelete all {result} (Y/N)? ").lower()
    if confirm == 'y':
        for root, dirs, files in walk(path_to_delete):
            if dirs:
                for dir in tqdm(dirs, unit=" dir", desc="Deleting dirs"):
                    rmtree(path.join(root, dir), ignore_errors=True)
            for file in tqdm(files, unit=" file", desc="Deleting files"):
                remove(path.join(root, file))


if __name__ == '__main__':
    main()
