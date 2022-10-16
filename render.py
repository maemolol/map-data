import json
from argparse import ArgumentParser
from glob import glob
from pathlib import Path

import vector
from renderer.render import prepare_render, render_part1, render_part2, render_part3
from renderer.types.pla2 import Pla2File
from renderer.types.zoom_params import ZoomParams


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


def main():
    parser = ArgumentParser()
    parser.add_argument("-n", '--namespaces', nargs="+", default=[])
    args = parser.parse_args()

    renders = []
    if args.namespaces:
        for ns in args.namespaces:
            renders.extend(Pla2File.from_file(Path(f"files/{ns}.pla2.msgpack")).components)
    else:
        for file in glob("files/*"):
            renders.extend(Pla2File.from_file(Path(file)).components)
    renders = list({(c.namespace, c.id): c for c in renders}.values())
    renders = Pla2File(
        namespace="",
        components=renders
    )

    print(f"Rendering {', '.join(args.namespaces) or 'everything'}")
    zoom = ZoomParams(0, 9, 32)
    export_id = ",".join(args.namespaces) if args.namespaces else "all"

    if get_batch(export_id) == -1:
        prepare_render(renders, zoom, export_id,
                       offset=vector.obj(x=0, y=32))
        set_batch(export_id, 0)
    if get_batch(export_id) == 0:
        render_part1(zoom, export_id, batch_size=8, chunk_size=4)
        set_batch(export_id, 1)
    if get_batch(export_id) == 1:
        render_part2(export_id, Path("./temp"))
        set_batch(export_id, 2)
    if get_batch(export_id) == 2:
        render_part3(export_id, save_dir=Path("./tiles"))
        set_batch(export_id, -1)


if __name__ == "__main__":
    main()
