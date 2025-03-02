import glob
import sys
from collections.abc import Iterator

import imagehash
import numpy as np
import numpy.typing as npt
from PIL import Image
from tqdm import tqdm


def zigzag_scan(m: npt.ArrayLike) -> Iterator:
    # upper left
    for i in range(len(m)):
        if i % 2 == 0:
            for j in range(i + 1):
                yield m[i - j][j]
        else:
            for j in range(i + 1):
                yield m[j][i - j]
    # lower right
    for j in range(1, len(m[0])):
        if j % 2 == 0:
            for d in range(0, len(m[0]) - j):
                yield m[j + d][len(m) - 1 - d]
        else:
            for d in range(0, len(m[0]) - j):
                yield m[len(m) - 1 - d][j + d]


def hash_zigzag(phash: int) -> int:
    b = bin(phash)[2:]
    return int(
        "".join(zigzag_scan(np.array([b[i] for i in range(len(b))]).reshape(8, 8))), 2
    )


def main() -> None:
    target_dir = sys.argv[1]
    target_files = glob.glob(target_dir + "/*.jpg")
    print("file_path,phash,phash_zigzag")
    for target_file in tqdm(target_files):
        phash = int(str(imagehash.phash(Image.open(target_file))), 16)
        print(",".join((target_file, str(phash), str(hash_zigzag(phash)))))


if __name__ == "__main__":
    main()
