from dotenv import load_dotenv
import os
import kagglehub

load_dotenv()

kaggle_api_key = os.environ.get("KAGGLE_API_KEY")

download_path = input("Enter the path into which you want to download the dataset: ")

os.environ["KAGGLEHUB_CACHE"] = download_path

dataset_path = kagglehub.dataset_download(
    "thedevastator/online-retail-sales-and-customer-data"
)

print("Path to dataset: ", dataset_path)
