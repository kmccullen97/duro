import sys
import os
import yaml

sys.path.append(os.getcwd())

from duro.config import default_config  # noqa E402

default_config["data_file"] = "path/to/data/file"

with open("./docs/default.yml", "w") as f:
    f.write(yaml.dump(default_config))
