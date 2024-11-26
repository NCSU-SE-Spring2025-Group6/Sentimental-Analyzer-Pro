# <img src="https://github.com/ychen-207523/Sentimental-Analyzer-Pro/blob/master/sentimental_analysis/realworld/static/images/logo-black-2.png" height="42" width="42"/>The Sentimental Analyzer Pro
## Software Engineering Project for CSC 510

[![DOI](https://zenodo.org/badge/869224666.svg)](https://doi.org/10.5281/zenodo.14004708)
[![GitHub Release](https://img.shields.io/github/v/release/jayjoshi1400/Sentimental-Analyzer-Pro)](https://github.com/jayjoshi1400/Sentimental-Analyzer-Pro/releases)
[![Build](https://github.com/jayjoshi1400/Sentimental-Analyzer-Pro/actions/workflows/main.yml/badge.svg)](https://github.com/jayjoshi1400/Sentimental-Analyzer-Pro/actions/workflows/main.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-v3.11+-brightgreen.svg)](https://www.python.org/)
[![GitHub contributors](https://img.shields.io/github/contributors/jayjoshi1400/Sentimental-Analyzer-Pro)](https://github.com/jayjoshi1400/Sentimental-Analyzer-Pro/graphs/contributors)
![GitHub Issues](https://img.shields.io/github/issues/jayjoshi1400/Sentimental-Analyzer-Pro)
![GitHub closed issues](https://img.shields.io/github/issues-closed/jayjoshi1400/Sentimental-Analyzer-Pro)
[![GitHub Issues or Pull Requests](https://img.shields.io/github/issues-pr/jayjoshi1400/Sentimental-Analyzer-Pro)](https://github.com/jayjoshi1400/Sentimental-Analyzer-Pro/pulls)
![GitHub language count](https://img.shields.io/github/languages/count/jayjoshi1400/Sentimental-Analyzer-Pro)
![GitHub repo size](https://img.shields.io/github/repo-size/jayjoshi1400/Sentimental-Analyzer-Pro)
[![github workflow](https://github.com/jayjoshi1400/Sentimental-Analyzer-Pro/actions/workflows/code_coverage.yml/badge.svg)](https://github.com/jayjoshi1400/Sentimental-Analyzer-Pro/actions/workflows/code_coverage.yml)
[![codecov](https://codecov.io/github/ychen-207523/Sentimental-Analyzer-Pro/graph/badge.svg?token=Z1S83G1x2E)](https://codecov.io/github/ychen-207523/Sentimental-Analyzer-Pro)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![autopep8](https://img.shields.io/badge/code_formatter-autopep8-blue)](https://pypi.org/project/autopep8/)
[![Static Badge](https://img.shields.io/badge/code_analysis-pylint-yellow?labelColor=grey)](https://pypi.org/project/pylint/)

---
The Sentimental Analyzer Pro is a versatile tool that can perform sentiment analysis on different types of data, including text, audio, reviews, and news articles. Sentiment analysis is one of the fastest-growing research areas in computer science, making it challenging to keep track of all the activities in the area. In our project, we aim to achieve our goal of accurately predicting a user's sentiment by analyzing the data provided using different types of input data.

## Working Demo

[![Watch the video](https://img.youtube.com/vi/rQOJ5UGA8WI/maxresdefault.jpg)](https://www.youtube.com/watch?v=rQOJ5UGA8WI)

---
 
## Table of Contents
1. [Introduction](#intro)
2. [Sentimental Analyzer Pro Features](#feat)
3. [How to use  Sentimental Analyzer Pro?](#exec)
4. [Roadmap and Progress](#roadmap)
5. [Case Study](#casestudy)
6. [Contributing to the product](#contribute)
7. [Connect with us](#Connectwithus)
8. [Team Members](#team)

---
<a name="intro"></a>
## Introduction

### What is Sentimental Analyzer Pro?
Sentiment analysis, also known as opinion mining, is the process of determining the sentiment or emotional tone in a piece of text, audio, or other forms of data. It involves identifying whether the sentiment expressed is positive, negative, or neutral.

### Why is it important?
<ul>
  <li>Sentiment analysis can help businesses and organizations understand how their customers or users feel about their products, services, or experiences. </li>
  <li>Companies can gauge public opinion about their products or services, track trends, and identify emerging issues or opportunities in the market.</li>
  <li>News agencies and media companies use sentiment analysis to analyze public sentiment towards news articles or events. This helps in generating content that aligns with the interests of the audience.</li>
  <li>Sentiment analysis is used in politics to understand public sentiment towards political candidates, parties, or policies. It is also used to gauge public opinion on social issues.</li>
</ul>

### Why use Sentimental Analyzer Pro?

The Sentimental Analyzer provides the following:
<ul>
  <li><b>Comprehensive Insights: </b>Different types of data sources provide diverse perspectives. An all-encompassing tool can provide a more comprehensive understanding of public sentiment.</li>
  <li><b>Multichannel Data Analysis:</b> In today's world, opinions and sentiments are expressed across various channels, including social media, customer reviews, audio recordings, and news articles. A tool that can analyze these diverse data sources offers a more accurate picture of public sentiment.</li>
  <li><b>Cost-Efficiency:</b> Instead of using multiple specialized tools, a single tool that can handle multiple data types is cost-effective and streamlines the analysis process.</li>
</ul>

![meme](https://github.com/ychen-207523/Sentimental-Analyzer-Pro/blob/master/assets/images/sentiment_analysis.jpg)

### How was Sentimental Analyzer Pro developed?
The complete development was achieved using the following technologies:
- Python3
- Django
- HTML
- CSS
- Scrapy
- Vader Analysis Tool
- Tensorflow

Although HTML and CSS are used for the front end, the users can merge the backend logic with any of the front end frameworks they wish to use such as React, and AngularJS.

---

<a name="feat"></a>
## What can Sentimental Analyzer Pro do?
|Feature|Description  |
|--|--|
|Product Analysis |```Sentimental analysis of Amazon product reviews```|
|News Analysis  |```Sentimental analysis of any recent news topic```|
|Text Analysis | ```Sentimental analysis of text input```|
|Audio Analysis   |``` Sentimental analysis of audio file``` |
|File Analysis   |``` Sentimental analysis of text file``` |
|Live Sentimental Analysis   |``` Sentimental analysis of live recorded audio``` |
|Facebook Post Analysis   |``` Sentimental analysis of Facebook Post``` |
|Twitter Post Analysis   |``` Sentimental analysis of Twitter Post``` |
|Reddit Post Analysis   |``` Sentimental analysis of Reddit Post``` |
---

<a name="exec"></a>
## How to use Sentimental Analyzer Pro?
### Installation
1. Clone this project:
```
git clone https://github.com/jayjoshi1400/Sentimental-Analyzer-Pro.git 
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
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"
```
5. Install ffmpeg:  
For Windows:  
```
winget install ffmpeg
```  
For Linux (Ubuntu):  
```
sudo apt install ffmpeg
```  
For Mac:  
```
brew install ffmpeg
```   
6. Run the migrations and start the Django Server using manage.py (Note: Make sure you are in root directory of the project.)
```
python3 ./sentimental_analysis/manage.py makemigrations
python3 ./sentimental_analysis/manage.py migrate
python3 ./sentimental_analysis/manage.py runserver
```
7. Next, open your browser and type in `localhost:8000` in the search bar to open the user interface of the application.
   
Now, you are good to go.

![](https://media.giphy.com/media/AgrfqPt5AyiTm/giphy.gif)

### Tests
To run the frontend tests, use the following command:
```
python3 sentimental_analysis/manage.py test realworld
```
To run the backend tests, use the following command:
```
pytest
```

### Usage

<a name="usecases"></a>
- Start the django server to get to the homepage<br><br>
![First](https://github.com/ychen-207523/Sentimental-Analyzer-Pro/blob/master/assets/gifs/Startup.gif)<br>

- Facebook Analysis<br><br>
![Second](<https://github.com/ychen-207523/Sentimental-Analyzer-Pro/blob/master/assets/gifs/FacebookAnalysis compressed.gif>)<br>

- Product Analysis<br><br>
![Third](<https://github.com/ychen-207523/Sentimental-Analyzer-Pro/blob/master/assets/gifs/Product Analysis Compressed (1) (2).gif>)<br>

- Twitter Analysis<br><br>
![Fourth](<https://github.com/ychen-207523/Sentimental-Analyzer-Pro/blob/master/assets/gifs/TwitterAnalysis comp.gif>)<br>

- Text Analysis<br><br>
![Fifth](<https://github.com/ychen-207523/Sentimental-Analyzer-Pro/blob/master/assets/gifs/TextAnalysis compressed.gif>)<br>

- Image to Document<br><br>
![Sixth](<https://github.com/ychen-207523/Sentimental-Analyzer-Pro/blob/master/assets/gifs/ImageToDocument compress.gif>)<br>

---
<a name="roadmap"></a>
## Roadmap and Progress
### Past Achievement(Previous Work)
- [x] Live Sentiment Analysis Feature inclusion
- [x] News Analysis Feature inclusion
- [x] Fixed and enhanced Amazon Product Analysis
- [x] Unit Tests were written and Test Coverage was improved

### Current Achievements
☑️  Implement User Authentication to store the login history of each User<br>
☑️  Visualize the sentiment distribution by each user comment for product analysis<br>
☑️  Upgraded news analysis by transitioning from Google Search to Google News scraping, yielding more relevant insights<br>
☑️  UI Improvement for enriching User interaction with the Application<br>
☑️  Enhance the Product Analysis by considering the number of users rated for each Product!<br>
☑️  Documentation Improvement for reflecting project's value accurately<br>
☑️  Addition of Builds and Workflows for better development activities<br>
☑️  Public facing webpage to get feedbacks, Raise and handle issues, Discuss & Grow with enthusiasts and supportive community<br>  

### Future Scope
- [ ] Recommendation System based on Product Analysis Results
- [ ] Add support for web scraping of dynamic, JavaScript-heavy sites to enhance data extraction
- [ ] Provide support for more platforms for social media analysis
      
---  
<a name="casestudy"></a>
## Case Study: Amazon Product Review Sentiment and Text Analysis
We have done a Case Study for our Sentiment Analysis Project. It can be found [here](https://github.com/NehaSJ99/Sentimental-Analyzer-Pro/blob/master/Case_Study.md).

---
<a name="contribute"></a>
## Eager to Contribute?
To Contribute to our application, please refer to [CONTRIBUTING.md](https://github.com/jayjoshi1400/Sentimental-Analyzer-Pro/blob/master/CONTRIBUTING.md)

---
<a name="Connectwithus"></a>
## Connect with us 
- Want to share your feedback or raise any issue [click here](https://noteforms.com/forms/sentiment-analyzer-pro-vkc5za)
- Need instant help? discuss over community chat to get help from other community members
- Join our mailing list for regular updates
- Join our discord forum for updates or support or discussions. [Join Here!](https://discord.gg/n8AuYxpf)
- Or just want to be part of our journey and get to know more about the Sentiment Analyser Pro and its team

**Visit our web page to be part of [Sentiment Analyser Pro community](https://elemental-gong-941.notion.site/Team22-Sentimental-Analyzer-Pro-130bc406342580f6bc05fcc486529b93)**

---

<a name="team"></a>
## Team Members

- Jay Joshi
- Dinesh Pasupuleti
- Srivradhan Vura

## Citation

This project is a fork of [Sentimental-Analyzer-Pro](https://github.com/NehaSJ99/Sentimental-Analyzer-Pro) by ***NehaSJ99***.<br>
Forked on: ***14 Nov 2024***<br>
Original Commit Hash: ***d11a4871660aa0a26f31764d150c87f2bd5d0586***

**Note:** This is an unfunded, non-profit project created for educational purposes.
