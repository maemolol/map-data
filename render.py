import io
import os
from argparse import ArgumentParser
from glob import glob
from pathlib import Path

import PIL.Image
from tile_renderer.render_tiles import render_tiles
from tile_renderer.coord import Coord
from tile_renderer.pla2 import Pla2File
# noinspection PyProtectedMember
from tile_renderer.skin import Skin


def main():
    parser = ArgumentParser()
    parser.add_argument("-n", "--namespaces", nargs="+", default=[])
    parser.add_argument("-z", "--zooms", nargs="+", type=int, default=[])
    args = parser.parse_args()

    renders = []
    if args.namespaces:
        for ns in args.namespaces:
            renders.extend(Pla2File.from_file(Path(f"files/{ns}.pla2.msgpack")).components)
    else:
        for file in glob("files/*"):
            renders.extend(Pla2File.from_file(Path(file)).components)
    renders = list({(c.namespace, c.id): c for c in renders}.values())

    print(f"Rendering {', '.join(args.namespaces) or 'everything'}")

    for zoom in args.zooms or (0, 1, 2, 3, 4, 5, 6, 7, 8, 9):
        for tile, b in render_tiles(
            components=renders,
            skin=Skin.default(),
            zoom=zoom,
            max_zoom_range=32,
            tile_size=256,
            offset=Coord(-0.5, -32),
            processes=os.cpu_count() + 1,
            chunk_size=16,
        ).items():
            path = Path(__file__).parent / "tiles" / str(9 - tile.z) / str(tile.x) / (str(tile.y) + ".webp")
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_bytes(b)
            try:
                PIL.Image.open(io.BytesIO(b)).save(path)
            except PIL.UnidentifiedImageError as e:
                raise ValueError(b) from e


if __name__ == "__main__":
    main()
