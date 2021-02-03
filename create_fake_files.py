"""Create 10 fake files postfixed with a varying serial number.

Call this script with an argument int. The argument represents the series.
If the script is called with a "0", created files will have names from
file_00_0.zip to file_00_9.zip. If the argument is "1" file names will go from
file_01_0.zip to file_01_9.zip. And so on.

All files are a copy of the example.csv file, in the data directory. Created files will be placed in the data/inbox directory.
"""

import os
from shutil import copyfile
import sys

from app import config


SEED_FILE_PATH = config.DATA_PATH / "example.csv"


def main(series: int):
    if not os.path.exists(config.INBOX_PATH):
        os.mkdir(config.INBOX_PATH)
    for i in range(0, 9):
        filename = f"file_%02d_{i}.csv" % series
        copyfile(SEED_FILE_PATH, config.INBOX_PATH / filename)
    print(f"Created files from file_%02d_0.csv to file_%02d_9.csv." % (
        series, series ))

if __name__ == "__main__":
    if len(sys.argv) == 2:
        try:
            main(int(sys.argv[1]))
            sys.exit(0)
        except ValueError:
            pass

    # If not an int argument, or missing argument.
    print(__doc__)
    print(f"Usage: {sys.argv[0]} <series>")
    print(f"\t <series> must be an int.")
    sys.exit(1)