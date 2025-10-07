from dotenv import load_dotenv
import os
import kagglehub
import shutil

load_dotenv()
kaggle_api_key = os.environ.get("KAGGLE_API_KEY")
download_path = "./data/raw"
os.environ["KAGGLEHUB_CACHE"] = download_path
dataset_path = kagglehub.dataset_download(
    "thedevastator/online-retail-sales-and-customer-data"
)

source_path = (
    download_path
    + "/datasets/thedevastator/online-retail-sales-and-customer-data/versions/1/online_retail.csv"
)
destination_path = "./data/raw"
shutil.copy(source_path, destination_path)
shutil.rmtree(download_path + "/datasets")
