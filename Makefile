prepare:
	@echo Creating folders for storing data 
	@mkdir data\raw data\interim data\processed

download:
	@echo Downloading the dataset
	@py src\download_dataset.py

clean:
	@echo Cleaning the data
	@py src\cleaning.py

delete:
	@echo Deleting irrelevant data
	@py src\data_preparation.py

outlier:
	@echo Removing outliers
	@py src\outlier_removal.py

features:
	@echo Calculating KPIs
	@py src\KPI.py

cluster:
	@echo Clustering the SKUs
	@py src\clustering.py

cleanup:
	@echo Removing unnecessary created folders
	@rmdir /s /q data\raw
	@rmdir /s /q data\interim

all: prepare download clean delete outlier features cluster cleanup