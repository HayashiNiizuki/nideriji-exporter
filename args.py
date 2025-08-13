import argparse


parser = argparse.ArgumentParser(
    description="exporter of nideriji.cn",
    formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument(
    "--save-diaries", action="store_true", default=False, help="save diaries file"
)

args = parser.parse_args()
del parser
