import gc
import json
from argparse import ArgumentParser
from copy import deepcopy
from glob import glob
from pathlib import Path

import psutil
import ray
import renderer
from renderer.tools import components

import sort_output


def read_file(path) -> dict:  # extract from JSON as dict
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data

def get_batch(ns: list[str]) -> int:
    with open("batchprogress.json", "r") as f:
        data = json.load(f)
        return data.get(','.join(ns), -1)

def set_batch(ns: str, batch: int):
    with open("batchprogress.json", "r+") as f:
        data = json.load(f)
        if batch != -1:
            data[','.join(ns)] = batch
        else:
            del data[','.join(ns)]
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=2)


def main():
    all_node_json = {}
    all_comps_json = {}
    for node_file in glob("nodes/*"):
        all_node_json.update(read_file(node_file))
    for comp_file in glob("comps/*"):
        all_comps_json.update(read_file(comp_file))

    parser = ArgumentParser()
    parser.add_argument("-n", '--namespaces', nargs="+", default=[])
    args = parser.parse_args()

    if args.namespaces:
        rendered_node_json = {}
        rendered_comps_json = {}
        for ns in args.namespaces:
            rendered_node_json.update(read_file(f"nodes/{ns}.nodes.pla"))
            rendered_comps_json.update(read_file(f"comps/{ns}.comps.pla"))
    else:
        rendered_node_json = all_node_json
        rendered_comps_json = all_comps_json

    all_nodes = renderer.NodeList(all_node_json)
    all_comps = renderer.ComponentList(all_comps_json, all_node_json)
    rendered_nodes = renderer.NodeList(rendered_node_json)
    rendered_comps = renderer.ComponentList(rendered_comps_json, rendered_node_json)

    print(f"Rendering {', '.join(args.namespaces) or 'everything'}")

    tiles = components.rendered_in(rendered_comps, rendered_nodes, 0, 9, 32)
    print(f"{len(tiles)} tiles to render")

    last_batch = get_batch(args.namespaces)

    for i, batch in enumerate(tiles[x:x + 1000] for x in range(0, len(tiles), 1000)):
        if i <= last_batch: continue
        print(f"Batch {i} of {int(len(tiles) // 1000)}")
        renderer.render(deepcopy(all_comps), deepcopy(all_nodes), renderer.ZoomParams(0, 9, 32),
                        save_dir=Path("./tiles"), offset=renderer.Coord(0, 32),
                        tiles=batch, use_ray=True, processes=psutil.cpu_count()//2)

        sort_output.main()
        ray.shutdown()
        gc.collect()
        set_batch(args.namespaces, i)
    set_batch(args.namespaces, -1)

if __name__ == "__main__": main()
