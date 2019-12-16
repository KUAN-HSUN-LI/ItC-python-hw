import argparse
from datetime import datetime


def get_args():
    # TODO: Add --start-date, --end-date and --output arguments
    #       Convert the two dates to datetime objects
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-date", default="2019-01-01", help="format: [Year-Month-Day] ex:2019-01-01")
    parser.add_argument("--end-date", default="2019-12-31", help="format: [Year-Month-Day] ex:2019-12-31")
    parser.add_argument("--output", default="output.csv", help="a output csv file")
    args = parser.parse_args()
    return args
