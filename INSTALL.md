<a name="exec"></a>
## How to use Sentimental Analyzer Pro?
### Installation
1. Clone this project:
```
git clone https://github.com/ychen-207523/Sentimental-Analyzer-Pro.git 
```
2. Make sure you are using Python 3.10 or higher. You can get it here: https://www.python.org/downloads/release/python-3115/

3. Create a Virtual Environment 
```
python3.10 -m venv env
source env/bin/activate
```
4. Install dependencies for the project from the root directory of the project:
```
pip3 install -r requirements.txt
```
5. Install other required module
```
pip3 install tf-keras
pip3 install spanish_nlp
pip3 install unidecode
```
6. Install ffmpeg:  
For Windows:  
```
winget install ffmpeg
```  
For Linux (Ubuntu):  
```
sudo apt install ffmpeg
```  
For Mac:  
*For brew installation help, checkout [Brew Installation help](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-homebrew-on-macos)*
```
brew install ffmpeg
```   
7. Run Django Server using manage.py (Note: Make sure you are in root directory of the project.)
```
python3 .\sentimental_analysis\manage.py runserver
```
8. Next, open your browser and type in `localhost:8000` in the search bar to open the user interface of the application.
   
Now, you are good to go.

![](https://media.giphy.com/media/AgrfqPt5AyiTm/giphy.gif)

### Usage

<a name="usecases"></a>
- Start the django server to get to the homepage
![First](https://github.com/ychen-207523/Sentimental-Analyzer-Pro/blob/master/assets/gifs/Startup.gif)
