import os
import re
import shutil
from glob import glob
from pathlib import Path

from tqdm import tqdm


def main():
    for tile in tqdm(glob("./tiles/*")):
        tile: str
        regex = re.search(r"[\\/](-?\d+), (-?\d+), (-?\d+)\.png", tile)
        if regex is None: continue
        z, x, y = regex.group(1), regex.group(2), regex.group(3)
        Path(f"./tiles/{z}/{x}").mkdir(parents=True, exist_ok=True)
        shutil.move(tile, Path(f"./tiles/{z}/{x}"))
        os.remove(Path(f"./tiles/{z}/{x}/{y}.png"))
        os.rename(Path(f"./tiles/{z}/{x}")/Path(tile).name, Path(f"./tiles/{z}/{x}/{y}.png"))

if __name__ == "__main__":
    main()