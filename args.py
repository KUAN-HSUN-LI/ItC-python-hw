import argparse


def get_args():
    """ Implentation arguments of crawler including start-date, end_date and output"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-date", type=valid_date, default="2019-01-01", help="format: [Year-Month-Day] ex:2019-01-01")
    parser.add_argument("--end-date", type=valid_date, default="2019-12-31", help="format: [Year-Month-Day] ex:2019-12-31")
    parser.add_argument("--output", type=str, default="output.csv", help="a output csv file")
    args = parser.parse_args()
    return args


def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = f"Not a valid date: {s}."
        raise argparse.ArgumentTypeError(msg)
