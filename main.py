import os

import argparse
import pandas as pd

from src.data.data_collect import data_collection
from src.data.data_process import data_preprocess


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scrape",
        help="Scrape climate bbc data.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--preprocess",
        help="Process collected data.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--web_app",
        help="Display streamlit web page.",
        action="store_true",
        default=False,
    )
    args = parser.parse_args()
    return args


args = get_args()

if args.scrape:
    link, author, date, text, images = data_collection()

    data = {
        "link": link,
        "author": author,
        "date": date,
        "text": text,
        "images": images,
    }
    print('Build dataset')
    dataset = pd.DataFrame(data)
    dataset.to_csv("dataset/climate_bbc_dataset.csv")

if args.preprocess:
    df = data_preprocess('dataset/climate_bbc_dataset.csv')
    df.to_csv('./dataset/process_data.csv')

if args.web_app:
    os.system("streamlit run ./app.py")
