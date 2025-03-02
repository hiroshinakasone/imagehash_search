import sys

import pandas as pd


def main():
    input_file = sys.argv[1]
    csv = pd.read_csv(input_file)
    csv.sort_values(by=["distance", "file1", "file2"], ascending=True, inplace=True)
    csv["image1"] = csv["file1"].apply(lambda x: f"<img src='{x}' width='400px'>")
    csv["image2"] = csv["file2"].apply(lambda x: f"<img src='{x}' width='400px'>")
    with open(f"{input_file}.html", "w") as f:
        f.write(csv.to_html(index=False, escape=False))


if __name__ == "__main__":
    main()
