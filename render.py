import gc
import json
import sys
from glob import glob
from pathlib import Path

import ray
import renderer
from renderer.tools import components

import sort_output


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

    tiles = components.rendered_in(comps, nodes, 0, 9, 32)
    print(f"{len(tiles)} tiles to render")

    for i, batch in enumerate(tiles[x:x + 1000] for x in range(0, len(tiles), 1000)):
        print(f"Batch {i} of {int(len(tiles) // 1000)}")
        renderer.render(comps, nodes, renderer.ZoomParams(0, 9, 32),
                        save_dir=Path("./tiles"), offset=renderer.Coord(0, 32),
                        tiles=batch, use_ray=True)

        sort_output.main()
        ray.shutdown()
        gc.collect()

if __name__ == "__main__": main()
