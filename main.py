from crawler import Crawler
from args import get_args
import pandas as pd

if __name__ == '__main__':
    args = get_args()
    crawler = Crawler()
    contents = crawler.crawl(args.start_date, args.end_date)
    df = pd.DataFrame(contents)
    df.to_csv(args.output, encoding="utf-8-sig", index=0)
