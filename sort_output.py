import os
import re
import shutil
from glob import glob
from pathlib import Path

from tqdm import tqdm


def main():
    for tile in tqdm(glob("./tiles/*"), desc="Sorting tiles"):
        tile: str
        regex = re.search(r"[\\/](-?\d+), (-?\d+), (-?\d+)\.webp", tile)
        if regex is None: continue
        z, x, y = regex.group(1), regex.group(2), regex.group(3)
        Path(f"./tiles/{z}/{x}").mkdir(parents=True, exist_ok=True)
        shutil.move(tile, Path(f"./tiles/{z}/{x}"))
        try:
            os.remove(Path(f"./tiles/{z}/{x}/{y}.webp"))
        except Exception: pass
        os.rename(Path(f"./tiles/{z}/{x}")/Path(tile).name, Path(f"./tiles/{z}/{x}/{y}.webp"))

if __name__ == "__main__":
    main()
