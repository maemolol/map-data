import json
import os
import re
import shutil
import sys
from glob import glob
from pathlib import Path

import renderer
from tqdm import tqdm


def read_file(path) -> dict:  # extract from JSON as dict
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data

def main():
    node_json = {}
    comps_json = {}
    if sys.argv[1:]:
        for ns in sys.argv[1:]:
            node_json.update(read_file(f"nodes/{ns}.nodes.pla"))
            comps_json.update(read_file(f"comps/{ns}.comps.pla"))
    else:
        for node_file in glob("nodes/*"):
            node_json.update(read_file(node_file))
        for comp_file in glob("comps/*"):
            comps_json.update(read_file(comp_file))

    nodes = renderer.NodeList(node_json)
    comps = renderer.ComponentList(comps_json, node_json)

    print(f"Rendering {', '.join(sys.argv[1:]) or 'everything'}")

    renderer.render(comps, nodes, renderer.ZoomParams(0, 9, 32),
                    save_dir=Path("./tiles"), offset=renderer.Coord(0, 32), use_ray=False)

    for tile in tqdm(glob("tiles/*")):
        tile: str
        regex = re.search(r"tiles/(-?\d+), (-?\d+), (-?\d+)\.png", tile)
        if regex is None: continue
        z, x, y = regex.group(1), regex.group(2), regex.group(3)
        Path(f"./tiles/{z}/{x}").mkdir(parents=True, exist_ok=True)
        shutil.move(tile, Path(f"./tiles/{z}/{x}"))
        os.rename(f"./tiles/{z}/{x}/"+tile.removeprefix("tiles/"), f"./tiles/{z}/{x}/{y}.png")

if __name__ == "__main__": main()