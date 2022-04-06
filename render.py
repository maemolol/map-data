import json
import os
import re
import shutil
from glob import glob
from pathlib import Path

import renderer
from tqdm import tqdm


def read_file(path) -> dict:  # extract from JSON as dict
    with open(path, "r") as f:
        data = json.load(f)
        return data

def main():
    node_json = {}
    for node_file in glob("nodes/*"):
        node_json.update(read_file(node_file))
    nodes = renderer.NodeList(node_json)

    comps_json = {}
    for comp_file in glob("comps/*"):
        comps_json.update(read_file(comp_file))
    comps = renderer.ComponentList(comps_json, node_json)
    renderer.render(comps, nodes, 0, 8, 64, save_dir=Path("./tiles"), offset=renderer.Coord(0, 32))

    for tile in tqdm(glob("tiles/*")):
        tile: str
        regex = re.search(r"tiles/(-?\d+), (-?\d+), (-?\d+)\.png", tile)
        if regex is None: continue
        z, x, y = regex.group(1), regex.group(2), regex.group(3)
        Path(f"./tiles/{z}/{x}").mkdir(parents=True, exist_ok=True)
        shutil.move(tile, Path(f"./tiles/{z}/{x}"))
        os.rename(f"./tiles/{z}/{x}/"+tile.removeprefix("tiles/"), f"./tiles/{z}/{x}/{y}.png")

if __name__ == "__main__": main()