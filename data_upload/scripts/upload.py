import json
import argparse

from target.factory import parse_target, init_driver

class FileInfo:
    def __init__(self, path, target):
        self.path = path
        self.target = parse_target(target)
    
    def __str__(self):
        return "FileInfo(path={}, target={})".format(self.path, self.target)
    
    def export(self):
        self.target.export(self.path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path to the config file", required=True)
    
    args = parser.parse_args()
    config_path = args.config

    with open(config_path, "r") as reader:
        config = json.load(reader)
        init_driver(config['drivers'].items())

        for file_info in config['files']:
            file_info = FileInfo(file_info['path'], file_info['target'])
            file_info.export()