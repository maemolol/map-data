from argparse import ArgumentParser
from glob import glob
from pathlib import Path

import renderer.render
import psutil
from renderer.misc_types.coord import Vector
from renderer.misc_types.pla2 import Pla2File
from renderer.misc_types.config import Config
from renderer.misc_types.zoom_params import ZoomParams
from renderer.render import MultiprocessConfig


def main():
    parser = ArgumentParser()
    parser.add_argument("-n", '--namespaces', nargs="+", default=[])
    parser.add_argument("-z", '--zooms', nargs="+", type=int, default=[])
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

    config = Config(
        zoom=ZoomParams(0, 9, 32),
        temp_dir=Path("./temp"),
        export_id=",".join(args.namespaces) if args.namespaces else "all"
    )

    print(f"Rendering {', '.join(args.namespaces) or 'everything'}")

    renderer.render.render(
        renders,
        config,
        save_dir=Path("./tiles"),
        offset=Vector(0, 32),
        zooms=args.zooms or None,
        part3_mp_config=MultiprocessConfig(batch_size=2*psutil.cpu_count())
    )


if __name__ == "__main__":
    main()
