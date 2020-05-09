# BooruScraper
A Framework as well as some scrapers for anime style image hosting websites such as pixiv and danbooru

## Install Guide
### Windows
#### Downloading Python
1. Download Python (Version <=3.6) at https://www.python.org/downloads/
2. Install Python (Requires pip but it should be installed with python by default, you can make sure by going to `Customize Installation -> pip`)
#### Cloning the Repo
3. Download this repository by clicking the Green "Clone or download" button on the page (Use Download Zip)
4. Extract the downloaded zip
#### Installing Dependencies
5. You should see a list of files that includes `main.py, README.md` and most importantly **requirements.txt**
6. Open a command prompt session (either admin or non admin will work), by *holding left shift and right click in the folder* and choose **open powershell window here** OR **open command prompt here**
7. For people who launched shell with **admin privileges** use following command: `pip install -r .\requirements.txt`
If you launched command prompt using **normal user** use this command:  `pip install -r .\requirements.txt --user`

### Linux
1. You guys are good enough to figure it out yourself, but still note: python version 3.6 or above is required due to f-string expression

## User Guide
### Configuring and Running the scraper
1. An configuration directory already exist at: ./config
2. Open the scraper you want to config with your fav text editor
3. Please read the documentation for each scraper, some instructions in one scraper may not apply to others
4. After the scraper is properly configured, run main.py to start the scraper

## Framework Documentation
See Scraper/docs for framework documentation
