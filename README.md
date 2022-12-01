# Scrape App for MacOS 👾

Web scraping app made with pygame. At the moment, it's only a prospect app that will scrape companies from hitta.se and save to csv with few filter possibilities. Faster and easier to make prospect lists instead of copy and paste by yourself.

### Things to do / In progress

- [ ] Add game(s) to play while waiting for scraping to finnish
- [ ] Add allabolag.se for web scraping 
- [ ] Add eniro.se for web scraping
- [ ] Add IMDb to app (web scraping is done)

PyInstaller targets the current running architecture and OS so in this installation you will run pyinstaller to create app bundle.

## Installation 

Download zipped project -> move to /Desktop -> unzip 

* ### Install Python 3.10

#### From website [Python.org](https://www.python.org/downloads/) or with homebrew

```bash
brew install python@3.10
```

* ### Install Python libraries 

#### Change directory
```bash
cd ~/Desktop/SCRAPE_APP
```

#### Create virtual environment (optional)
```bash
python3 -m venv packenv 
source packenv/bin/activate
```

#### Install python libraries
```bash
pip3 install -r requirements.txt
```


## Create App

```bash
pyinstaller --windowed --name="Prospect" --icon="prospect_icon.icns" main.py
```

#### If app icon in dock not same as app icon

```bash
rm ~/Desktop/SCRAPE_APP/dist/Prospect.app/Contents/MacOS/pygame/pygame_icon_mac.bmp && mv ~/Desktop/SCRAPE_APP/prospect_icon.icns ~/Desktop/SCRAPE_APP/dist/Prospect.app/Contents/MacOS/pygame/pygame_icon_mac.bmp
```
