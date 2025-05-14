import sys
import dotenv
import os
import pathlib
import numpy as np
import random

dotenv.load_dotenv()
project_path = pathlib.Path(dotenv.find_dotenv()).parent
src_path = project_path.joinpath("src", "py")
sys.path.insert(0, src_path.as_posix())

print(sys.executable)
print(src_path)
print(os.environ["name"])
print(os.environ["uem_id"])

try:
    import db_parser
    print("paths ok")
except ImportError as err:
    print(err)

try:
    seed = int(os.environ["seed"])
    random.seed(seed)
    np.random.seed(seed)
except Exception as err:
    print(err)