from dotenv import load_dotenv
import os
import kagglehub
import shutil
import config

load_dotenv()
kaggle_api_key = config.kaggle_api_key
download_path = "./data/raw"
os.environ["KAGGLEHUB_CACHE"] = download_path
dataset_path = kagglehub.dataset_download(
    "thedevastator/online-retail-sales-and-customer-data"
)

source_path = (
    download_path
    + "/datasets/thedevastator/online-retail-sales-and-customer-data/versions/1/online_retail.csv"
)
shutil.copy(source_path, download_path)
shutil.rmtree(download_path + "/datasets")
