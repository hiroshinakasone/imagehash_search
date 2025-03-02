import sys
from typing import TextIO

import pandas as pd
from tqdm import tqdm


def hamming_distance(ph1: int, ph2: int) -> int:
    return bin(ph1 ^ ph2).count("1")


def output_distance(i: int, csv_rows: list[str], output_file: TextIO) -> None:
    if i % 1000 == 0 and len(csv_rows) > 0:
        output_file.write("\n".join(csv_rows))
        output_file.write("\n")
        csv_rows.clear()


def output_distance_histogram(c: dict[int, int], output_file_name: str) -> None:
    with open(output_file_name, "w") as f:
        f.write(f"combination N: {sum(c.values())}\n")
        for k in sorted(c.keys()):
            f.write(f"{k}: {c[k]}\n")
        f.write("\n")


def main():
    df, div = pd.read_csv(sys.argv[1]), int(sys.argv[2])
    distance_output_file = open(f"output_div{div}_distance.csv", "w")

    n = int(df.shape[0]) // div
    print(f"image N:{n}")

    c = {}
    csv_rows = ["distance,file1,file2"]
    for i in tqdm(range(n)):
        for j in range(i, n):
            if i == j:
                continue
            d = hamming_distance(df.iloc[i]["phash"], df.iloc[j]["phash"])
            if d <= 10:
                csv_rows.append(
                    f"{d},{df.iloc[i]['file_path']},{df.iloc[j]['file_path']}"
                )
                output_distance(i, csv_rows, distance_output_file)
            v = c.get(d, 0)
            c[d] = v + 1
    output_distance(0, csv_rows, distance_output_file)
    distance_output_file.close()

    output_distance_histogram(c, f"output_div{div}_distance_histogram.txt")


if __name__ == "__main__":
    main()
