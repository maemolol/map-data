import json
from argparse import ArgumentParser
from glob import glob
from pathlib import Path

import renderer


def get_batch(ns: str) -> int:
    with open("batchprogress.json", "r") as f:
        data = json.load(f)
        return data.get(ns, -1)

def set_batch(ns: str, batch: int):
    with open("batchprogress.json", "r+") as f:
        data = json.load(f)
        if batch != -1:
            data[ns] = batch
        else:
            del data[ns]
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=2)

def read_file(path) -> dict:  # extract from JSON as dict
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data


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

    rendered_nodes = renderer.NodeList(rendered_node_json)
    rendered_comps = renderer.ComponentList(rendered_comps_json, rendered_node_json)

    print(f"Rendering {', '.join(args.namespaces) or 'everything'}")
    zoom = renderer.ZoomParams(0, 9, 32)
    export_id = ",".join(args.namespaces) if args.namespaces else "all"

    if get_batch(export_id) == -1:
        renderer.base.prepare_render(rendered_comps, rendered_nodes, zoom, export_id,
                                     offset=renderer.Coord(0, 32))
        set_batch(export_id, 0)
    if get_batch(export_id) == 0:
        renderer.base.render_part1_ray(rendered_comps, rendered_nodes, zoom, export_id, batch_size=8)
        set_batch(export_id, 1)
    if get_batch(export_id) == 1:
        renderer.base.render_part2(export_id)
        set_batch(export_id, 2)
    if get_batch(export_id) == 2:
        renderer.base.render_part3_ray(export_id, save_dir=Path("./tiles"))
        set_batch(export_id, -1)

if __name__ == "__main__": main()
