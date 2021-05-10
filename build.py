#!/usr/bin/env python3

import os
from os.path import basename
import re
import yaml
import shutil
from zipfile import ZipFile

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


# credits: @TheMatt2
def walklevel(path, depth=1):
    """It works just like os.walk, but you can pass it a level parameter
     that indicates how deep the recursion will go.
     If depth is 1, the current directory is listed.
     If depth is 0, nothing is returned.
     If depth is -1 (or less than 0), the full depth is walked.
  """

    if depth < 0:
        for root, dirs, files in os.walk(path):
            yield root, dirs[:], files
        return
    elif depth == 0:
        return

    base_depth = path.rstrip(os.path.sep).count(os.path.sep)
    for root, dirs, files in os.walk(path):
        yield root, dirs[:], files
        cur_depth = root.count(os.path.sep)
        if base_depth + depth <= cur_depth:
            del dirs[:]


def zip_directory(zip_filename, directory):
    with ZipFile(zip_filename, 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(folderName, filename)
                zipObj.write(file_path, basename(file_path))


def run():
    pattern = re.compile(r'^\./[^.][^/]+/[^/]+$')
    for root, dirs, files in walklevel(path=".", depth=2):
        if pattern.match(root):
            challenge_key = basename(root)
            player_files_dir = f"{root}/player_files/"
            player_files_zip_current = f"./{challenge_key}.zip"
            player_files_zip_from_root = f"{root}/{challenge_key}.zip"
            instructions_file = f"{root}/documentation/instructions.txt"
            hint_file = f"{root}/documentation/hint.txt"
            manifest_file = f"{root}/documentation/manifest.yml"
            challenge_dot_yaml_file = f"{root}/challenge.yml"

            print(f">>>Preparing {root} for deployment to CTFd<<<")

            if os.path.exists(manifest_file):
                try:
                    print("INFO: reading manifest file.")
                    manifest = yaml.load(open(manifest_file), Loader=Loader)
                except yaml.YAMLError:
                    print(f"ERROR: Encountered a YAML parsing error when parsing {manifest_file}.")
                    continue
            else:
                print(f"ERROR: No manifest file found in {root}.")
                continue

            if os.path.exists(instructions_file):
                try:
                    print("INFO: reading instructions.txt file.")
                    instructions = open(instructions_file).read().replace("\n", "<br>")
                except OSError:
                    print(f"ERROR: Error reading: {instructions_file}.")
                    continue
                print("INFO: Adding content of instructions.txt to challenge metadata.")
                manifest.update({"description": instructions})
            else:
                print(f"ERROR: No instructions file found in the {root}/documentation/ directory.")
                continue

            if os.path.exists(hint_file):
                hint = None
                try:
                    print("INFO: reading hint.txt file.")
                    hint = open(hint_file).read().replace("\n", "<br>")
                except OSError:
                    print(f"ERROR: Error reading: {hint_file}.")
                hint_cost = manifest.get("hint_cost", None)
                if hint_cost is not None:
                    print("INFO: Adding content of hint.txt to challenge metadata.")
                    manifest.update({"hints": [{"content": hint, "cost": manifest["hint_cost"]}]})
                    manifest.pop("hint_cost", None)
                else:
                    print(f"ERROR: No hint_cost specified even though a hint file was found in the"
                          f" {root}/documentation/ directory.")
                    continue

            if os.path.exists(player_files_dir):
                print("INFO: Copying instructions.txt file into player_files directory.")
                shutil.copy(src=instructions_file, dst=player_files_dir)
                print(f"INFO: Zipping player_files directory into {player_files_zip_from_root}.")
                zip_directory(zip_filename=player_files_zip_from_root, directory=player_files_dir)
                print("INFO: Adding player files archive location to challenge metadata.")
                manifest.update({"files": [player_files_zip_from_root]})
            else:
                print(f"INFO: No player_files directory found for {challenge_key}.")

            stream = None
            try:
                stream = open(challenge_dot_yaml_file, "w")
            except OSError:
                print(f"ERROR: error creating/writing to {challenge_dot_yaml_file}.")
                continue

            try:
                print("INFO: Dumping challenge metadata into CTFd challenge.yml file.")
                yaml.dump(manifest, stream)
            except yaml.YAMLError:
                print("ERROR: An error occurred while dumping the challenge.yml file.")
                continue


if __name__ == '__main__':
    run()
