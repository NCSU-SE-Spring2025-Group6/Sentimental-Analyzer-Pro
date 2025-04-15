import os
import sys
import json
import csv
from io import StringIO
import subprocess
import shutil
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import speech_recognition as sr
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.template.defaulttags import register
from django.http import HttpResponse
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import nltk
from pydub import AudioSegment
from nltk.corpus import stopwords
from nltk import pos_tag
import cv2
from deepface import DeepFace
from langdetect import detect
from spanish_nlp import classifiers
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import (
    update_session_auth_hash,
    get_user
)
from .cache_manager import AnalysisCache
from .newsScraper import scrapNews
from .utilityFunctions import (
    removeLinks,
    stripEmojis,
    removeSpecialChar,
    stripPunctuations,
    stripExtraWhiteSpaces
)
from realworld.fb_scrap import fb_sentiment_score
from realworld.twitter_scrap import twitter_sentiment_score
from realworld.reddit_scrap import fetch_reddit_post, reddit_sentiment_score
from realworld.models import Profile
from realworld.history_manager import (
    store_text_analysis,
    store_image_analysis,
    store_news_analysis,
    store_document_analysis,
    store_audio_analysis,
    store_live_analysis,
    store_facebook_data,
    store_twitter_data,
    store_reddit_data,
    store_product_analysis,
    store_youtube_data
)
from realworld.youtube_scrap import get_transcript, get_top_liked_comments

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


@login_required
def update_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        messages.success(request, "Account updated successfully.")
        return redirect('profile')
    return render(request, 'realworld/profile.html')


@login_required
def update_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        two_fa_method = request.POST.get('2fa_method')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('profile')

        user = request.user
        user.username = username
        user.email = email
        user.set_password(password)
        user.save()

        # Re-authenticate the user to prevent logout
        update_session_auth_hash(request, user)

        profile, created = Profile.objects.get_or_create(user=user)
        profile.contact_number = contact_number
        profile.two_fa_method = two_fa_method
        profile.save()

        messages.success(request, "Account updated successfully.")
        return redirect('profile')
    return render(request, 'realworld/profile.html')


@login_required
def opt_out(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    profile.opted_out = True
    profile.save()
    messages.success(request,
                     "You have opted out of the"
                     "sale/sharing of your personal data.")
    return redirect('profile')


def delete_data(request):
    user = request.user
    directory_path = os.path.join("sentimental_analysis", "media", "user_data")
    file_path = os.path.join(directory_path, f"{user.username}.json")
    if os.path.exists(file_path):
        os.remove(file_path)
    messages.success(request,
                     "Your personal data has been deleted.")
    return redirect('profile')


def profile_view(request):
    return render(request, 'realworld/profile.html')


def settings_view(request):
    return render(request, 'realworld/settings.html')


from datetime import datetime

def history_view(request):
    user = get_user(request)
    username = user.username

    # Define the directory path
    directory_path = os.path.join(
        "sentimental_analysis",
        "media",
        "user_data"
    )
    file_path = os.path.join(directory_path, f"{username}.json")

    history_data = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            history_data = json.load(json_file)

        # Add formatted timestamp to each entry
        for section, records in history_data.items():
            for timestamp, record in records.items():
                try:
                    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    formatted = dt.strftime("%b %d, %Y at %I:%M %p")
                    record['formatted_time'] = formatted
                except Exception:
                    record['formatted_time'] = timestamp  # fallback

    # Flatten and sort the history data by timestamp
    sorted_history = []
    for section, records in history_data.items():
        for timestamp, data in records.items():
            sorted_history.append({
                'section': section,
                'timestamp': timestamp,
                'data': data
            })
    sorted_history.sort(key=lambda x: x['timestamp'], reverse=True)  # Sort by timestamp (most recent first)

    return render(
        request,
        'realworld/history.html',
        {'sorted_history': sorted_history}
    )

@csrf_exempt
@login_required
def delete_history_entry(request):
    if request.method == 'POST':
        timestamp = request.POST.get('timestamp')
        section = request.POST.get('section')

        user = get_user(request)
        username = user.username

        # Define the file path
        file_path = os.path.join(
            "sentimental_analysis",
            "media",
            "user_data",
            f"{username}.json"
        )

        if os.path.exists(file_path):
            with open(file_path, 'r') as json_file:
                history_data = json.load(json_file)

            # Remove the entry from the specified section
            if section in history_data and timestamp in history_data[section]:
                del history_data[section][timestamp]

                # Save the updated data back to the file
                with open(file_path, 'w') as json_file:
                    json.dump(history_data, json_file, indent=4)

                messages.success(request, "History entry deleted successfully.")
            else:
                messages.error(request, "History entry not found.")
        else:
            messages.error(request, "User history file not found.")

        return redirect('history')  # Redirect back to the history page


def pdfparser(data):
    fp = open(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data = retstr.getvalue()

    text_file = open("Output.txt", "w", encoding="utf-8")
    text_file.write(data)

    text_file = open("Output.txt", 'r', encoding="utf-8")
    a = ""
    for x in text_file:
        if len(x) > 2:
            b = x.split()
            for i in b:
                a += " " + i
    final_comment = a.split('.')
    return final_comment


@login_required
def analysis(request):
    return render(request, 'realworld/index.html')


def get_clean_text(text):
    text = removeLinks(text)
    text = stripEmojis(text)
    text = removeSpecialChar(text)
    text = stripPunctuations(text)
    text = stripExtraWhiteSpaces(text)
    tokens = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english')).union([
        'the', 'a', 'an', 'this', 'that', 'these', 'those', 'is',
        'are', 'was', 'were', 'be', 'been', 'being', 'have',
        'has', 'had', 'having', 'do', 'does', 'did', 'doing',
        'will', 'would', 'shall', 'should', 'can', 'could', 'may',
        'might', 'must', 'ought', 'it', 'they', 'them', 'their',
        'theirs', 'themselves', 'he', 'she', 'him', 'her',
        'his', 'hers', 'himself', 'herself', 'we', 'us', 'our',
        'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
        'yourselves', 'i', 'me', 'my', 'mine', 'myself'
    ])
    stop_words.add('rt')
    stop_words.add('')

    newtokens = [
        item for item, pos_tag in pos_tag(tokens)
        if (item.lower() not in stop_words and
            pos_tag in ['NN', 'VB', 'JJ', 'RB'])
    ]

    textclean = ' '.join(newtokens)
    return textclean


def detailed_analysis(result):
    result_dict = {}
    neg_count = 0
    pos_count = 0
    neu_count = 0

    for item in result:
        cleantext = get_clean_text(str(item))
        # print(cleantext)
        sentiment = sentiment_analyzer_scores(cleantext)
        pos_count += sentiment['pos']
        neu_count += sentiment['neu']
        neg_count += sentiment['neg']
    total = pos_count + neu_count + neg_count
    if total > 0:
        pos_ratio = pos_count / total
        neu_ratio = neu_count / total
        neg_ratio = neg_count / total
        result_dict['pos'] = pos_ratio
        result_dict['neu'] = neu_ratio
        result_dict['neg'] = neg_ratio
    return result_dict


def detailed_analysis_sentence(result):
    sia = SentimentIntensityAnalyzer()
    result_dict = {}
    result_dict['compound'] = sia.polarity_scores(result)['compound']
    return result_dict


def input(request):
    if request.method == 'POST':
        file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(file.name, file)
        pathname = 'sentimental_analysis/media/'
        extension_name = file.name
        extension_name = extension_name[len(extension_name) - 3:]
        path = pathname + file.name
        destination_folder = 'sentimental_analysis/media/document/'
        shutil.copy(path, destination_folder)
        useFile = destination_folder + file.name
        result = {}
        finalText = ''
        if extension_name == 'pdf':
            value = pdfparser(useFile)
            result = detailed_analysis(value)
            finalText = result
        elif extension_name == 'txt':
            text_file = open(useFile, 'r', encoding="utf-8")
            a = ""
            for x in text_file:
                if len(x) > 2:
                    b = x.split()
                    for i in b:
                        a += " " + i
            final_comment = a.split('.')
            text_file.close()
            finalText = final_comment
            result = detailed_analysis(final_comment)
        folder_path = 'sentimental_analysis/media/'
        files = os.listdir(folder_path)
        for file in files:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        store_document_analysis(
            request,
            data={
                'sentiment': result,
                'text': finalText,
                'reviewsRatio': {},
                'totalReviews': 1,
                'showReviewsRatio': False
            }
        )  # Store the analysis data in the user's history
        return render(
            request,
            'realworld/results.html',
            {
                'sentiment': result,
                'text': finalText,
                'reviewsRatio': {},
                'totalReviews': 1,
                'showReviewsRatio': False
            }
        )
    else:
        note = "Please Enter the Document you want to analyze"
        return render(request, 'realworld/home.html', {'note': note})


def inputimage(request):
    if request.method == 'POST':
        file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(file.name, file)
        pathname = 'sentimental_analysis/media/'
        extension_name = file.name
        extension_name = extension_name[len(extension_name) - 3:]
        path = pathname + file.name
        destination_folder = 'sentimental_analysis/media/document/'
        shutil.copy(path, destination_folder)
        useFile = destination_folder + file.name

        if os.path.exists(path):
            os.remove(path)

        image = cv2.imread(useFile)
        try:
            detected_emotion = DeepFace.analyze(image)
        except Exception as e:
            print(f"Error analyzing image: {e}")
            detected_emotion = []

        emotions_dict = {'happy': 0.0, 'sad': 0.0, 'neutral': 0.0}
        for emotion in detected_emotion:
            emotion_scores = emotion['emotion']
            happy_score = emotion_scores['happy']
            sad_score = emotion_scores['sad']
            neutral_score = emotion_scores['neutral']

            emotions_dict['happy'] += happy_score
            emotions_dict['sad'] += sad_score
            emotions_dict['neutral'] += neutral_score

        total_score = sum(emotions_dict.values())
        if total_score > 0:
            for emotion in emotions_dict:
                emotions_dict[emotion] /= total_score

        print(emotions_dict)
        finalText = max(emotions_dict, key=emotions_dict.get)

        store_image_analysis(
            request,
            data={
                'sentiment': emotions_dict,
                'text': finalText,
                'analyzed_image_path': useFile
            }
        )

        return render(
            request,
            'realworld/resultsimage.html',
            {
                'sentiment': emotions_dict,
                'text': finalText,
                'analyzed_image_path': useFile
            }
        )


def productanalysis(request):
    if request.method == 'POST':
        blogname = request.POST.get("blogname", "")

        text_file = open(
            "Amazon_Comments_Scrapper/amazon_reviews_scraping/"
            "amazon_reviews_scraping/spiders/ProductAnalysis.txt", "w")
        text_file.write(blogname)
        text_file.close()

        spider_path = (
            r'Amazon_Comments_Scrapper/amazon_reviews_scraping/'
            r'amazon_reviews_scraping/spiders/amazon_review.py'
        )
        output_file = (
            r'Amazon_Comments_Scrapper/amazon_reviews_scraping/'
            r'amazon_reviews_scraping/spiders/reviews.json'
        )
        command = f"scrapy runspider \"{spider_path}\" -o \"{output_file}\" "
        result = subprocess.run(command, shell=True)

        if result.returncode == 0:
            print("Scrapy spider executed successfully.")
        else:
            print("Error executing Scrapy spider.")

        with open(
            r'Amazon_Comments_Scrapper/amazon_reviews_scraping/'
            r'amazon_reviews_scraping/spiders/reviews.json',
            'r'
        ) as json_file:
            json_data = json.load(json_file)
        reviews = []
        reviews2 = {
            "pos": 0,
            "neu": 0,
            "neg": 0,
        }
        for item in json_data:
            reviews.append(item['Review'])
            r = detailed_analysis_sentence(item['Review'])
            if (r != {}):
                st = item['Stars']
                if (st is not None):
                    stars = int(float(st))
                    if (stars != -1):
                        if (stars >= 4):
                            r['compound'] += 0.1
                        elif (stars >= 2):
                            continue
                        else:
                            r['compound'] -= 0.1
                if (r['compound'] > 0.4):
                    reviews2['pos'] += 1
                elif (r['compound'] < -0.4):
                    reviews2['neg'] += 1
                else:
                    reviews2['neu'] += 1
        finalText = reviews
        totalReviews = reviews2['pos'] + reviews2['neu'] + reviews2['neg']
        result = detailed_analysis(reviews)
        store_product_analysis(
            request,
            data={
                'sentiment': result,
                'text': finalText,
                'reviewsRatio': reviews2,
                'totalReviews': totalReviews,
                'showReviewsRatio': True
            }
        )
        return render(
            request,
            'realworld/results.html',
            {
                'sentiment': result,
                'text': finalText,
                'reviewsRatio': reviews2,
                'totalReviews': totalReviews,
                'showReviewsRatio': True
            }
        )

    else:
        note = "Please Enter the product blog link for analysis"
        return render(
            request,
            'realworld/productanalysis.html',
            {'note': note}
        )


def textanalysis(request): # unused now
    if request.method == 'POST':
        text_data = request.POST.get("textField", "")
        final_comment = text_data.split('.')
        result = {}
        finalText = final_comment
        if determine_language(final_comment):
            result = detailed_analysis(final_comment)
        else:
            sc = classifiers.SpanishClassifier(
                model_name="sentiment_analysis"
            )
            result_string = ' '.join(final_comment)
            result_classifier = sc.predict(result_string)
            result = {
                'pos': result_classifier.get('positive', 0.0),
                'neu': result_classifier.get('neutral', 0.0),
                'neg': result_classifier.get('negative', 0.0)
            }
        store_text_analysis(
            request,
            data={
                    'sentiment': result,
                    'text': finalText,
                    'reviewsRatio': {},
                    'totalReviews': 1,
                    'showReviewsRatio': False
            }
        )
        return render(
            request,
            'realworld/results.html',
            {
                'sentiment': result,
                'text': finalText,
                'reviewsRatio': {},
                'totalReviews': 1,
                'showReviewsRatio': False
            }
        )
    else:
        note = "Enter the Text to be analysed!"
        return render(request, 'realworld/textanalysis.html', {'note': note})

def batch_analysis(request):
    if request.method == 'POST':
        full_text_data = request.POST.get("batchTextField", "")
        # sentences = full_text_data.split('.')
        sentences = nltk.sent_tokenize(full_text_data) # better than splitting by period (accomodates abbreviations like U.S.A.)
        results = []

        for sentence in sentences:
            cleaned_sentence = sentence.strip()
            if cleaned_sentence:
                if determine_language([cleaned_sentence]):
                    sentiment_result = detailed_analysis([cleaned_sentence])
                else:
                    sc = classifiers.SpanishClassifier(model_name="sentiment_analysis")
                    result_classifier = sc.predict(cleaned_sentence)
                    sentiment_result = {
                        'pos': result_classifier.get('positive', 0.0),
                        'neg': result_classifier.get('negative', 0.0),
                        'neu': result_classifier.get('neutral', 0.0)
                    }
                results.append({'text': cleaned_sentence, 'sentiment': sentiment_result})

        store_text_analysis(
            request,
            data={
                'sentiment': calculate_average_sentiment(results),
                'text': sentences,
                'reviewsRatio': {i: res for i, res in enumerate(results)}, # Store individual sentence results
                'totalReviews': len(results),
                'showReviewsRatio': True
            }
        )
        return render(
            request,
            'realworld/results.html',
            {
                'sentiment': calculate_average_sentiment(results),
                'text': sentences,
                'reviewsRatio': {i: res for i, res in enumerate(results)},
                'totalReviews': len(results),
                'showReviewsRatio': False
            }
        )
    else:
        note = "Enter the Text to be analysed!"
        return render(request, 'realworld/textanalysis.html', {'note': note})

def calculate_average_sentiment(results):
    if not results:
        return {'pos': 0.0, 'neg': 0.0, 'neu': 0.0}
    total_pos = sum(res['sentiment']['pos'] for res in results)
    total_neg = sum(res['sentiment']['neg'] for res in results)
    total_neu = sum(res['sentiment']['neu'] for res in results)
    num_results = len(results)
    return {
        'pos': total_pos / num_results,
        'neg': total_neg / num_results,
        'neu': total_neu / num_results
    }

def youtube_transcript_analysis(request):
    if request.method == 'POST':
        video_link = request.POST.get("vidlink", "")
        full_text_data = get_transcript(video_link=video_link)

        if not full_text_data:
            return 404 # link didn't work
        
        # sentences = full_text_data.split('.')
        sentences = nltk.PunktSentenceTokenizer().tokenize(full_text_data)
        results = []

        for sentence in sentences:
            cleaned_sentence = sentence.strip()
            if cleaned_sentence:
                if determine_language([cleaned_sentence]):
                    sentiment_result = detailed_analysis([cleaned_sentence])
                else:
                    sc = classifiers.SpanishClassifier(model_name="sentiment_analysis")
                    result_classifier = sc.predict(cleaned_sentence)
                    sentiment_result = {
                        'pos': result_classifier.get('positive', 0.0),
                        'neg': result_classifier.get('negative', 0.0),
                        'neu': result_classifier.get('neutral', 0.0)
                    }
                results.append({'text': cleaned_sentence, 'sentiment': sentiment_result})

        store_youtube_data(
            request,
            data={
                'sentiment': calculate_average_sentiment(results),
                'text': sentences,
                'reviewsRatio': {i: res for i, res in enumerate(results)}, # Store individual sentence results
                'totalReviews': len(results),
                'showReviewsRatio': True
            }
        )
        return render(
            request,
            'realworld/results.html',
            {
                'sentiment': calculate_average_sentiment(results),
                'text': sentences,
                'reviewsRatio': {i: res for i, res in enumerate(results)},
                'totalReviews': len(results),
                'showReviewsRatio': True
            }
        )
    else:
        note = "Enter link to yt video"
        return render(request, 'realworld/textanalysis.html', {'note': note})
    
def youtube_comments_analysis(request):
    if request.method == 'POST':
        video_link = request.POST.get("vidlink", "")
        full_text_data = get_top_liked_comments(video_link=video_link)

        if not full_text_data:
            return 404 # link didn't work
        
        # sentences = full_text_data.split('.')
        sentences = nltk.sent_tokenize(full_text_data)
        results = []

        for sentence in sentences:
            cleaned_sentence = sentence.strip()
            if cleaned_sentence:
                if determine_language([cleaned_sentence]):
                    sentiment_result = detailed_analysis([cleaned_sentence])
                else:
                    sc = classifiers.SpanishClassifier(model_name="sentiment_analysis")
                    result_classifier = sc.predict(cleaned_sentence)
                    sentiment_result = {
                        'pos': result_classifier.get('positive', 0.0),
                        'neg': result_classifier.get('negative', 0.0),
                        'neu': result_classifier.get('neutral', 0.0)
                    }
                if sentiment_result:
                    results.append({'text': cleaned_sentence, 'sentiment': sentiment_result})

        store_youtube_data(
            request,
            data={
                'sentiment': calculate_average_sentiment(results),
                'text': sentences,
                'reviewsRatio': {i: res for i, res in enumerate(results)}, # Store individual sentence results
                'totalReviews': len(results),
                'showReviewsRatio': True
            }
        )
        return render(
            request,
            'realworld/results.html',
            {
                'sentiment': calculate_average_sentiment(results),
                'text': sentences,
                'reviewsRatio': {i: res for i, res in enumerate(results)},
                'totalReviews': len(results),
                'showReviewsRatio': True
            }
        )
    else:
        note = "Enter link to yt video"
        return render(request, 'realworld/textanalysis.html', {'note': note})

def determine_language(texts):
    try:
        for text in texts:
            lang = detect(text)
            if lang != 'en':
                return False
        return True
    except Exception as e:
        # Handle potential exceptions when using langdetect
        print(f"Error detecting language: {e}")
        return False


def fbanalysis(request):
    if request.method == 'POST':
        current_directory = os.path.dirname(__file__)
        result = fb_sentiment_score()

        csv_file_fb = 'fb_sentiment.csv'
        csv_file_path = os.path.join(current_directory, csv_file_fb)

        # Open the CSV file and read its content
        with open(csv_file_path, 'r') as csv_file:
            # Use DictReader to read CSV data into a list of dictionaries
            csv_reader = csv.DictReader(csv_file)
            data = [row for row in csv_reader]

        text_dict = {"reviews": data}
        print("text_dict:", text_dict["reviews"])
        # Convert the list of dictionaries to a JSON array
        # json_data = json.dumps(text_dict, indent=2)

        reviews = []

        for item in text_dict["reviews"]:
            # print("item :",item)
            reviews.append(item["FBPost"])
        finalText = reviews

        store_facebook_data(
            request,
            data={
                'sentiment': result,
                'text': finalText,
                'reviewsRatio': {},
                'totalReviews': 1,
                'showReviewsRatio': False
            }
        )

        return render(
            request,
            'realworld/results.html',
            {
                'sentiment': result,
                'text': finalText,
                'reviewsRatio': {},
                'totalReviews': 1,
                'showReviewsRatio': False
            }
        )
    else:
        note = "Please Enter the product blog link for analysis"
        return render(
            request,
            'realworld/productanalysis.html',
            {'note': note}
        )


def twitteranalysis(request):
    if request.method == 'POST':
        current_directory = os.path.dirname(__file__)
        result = twitter_sentiment_score()

        csv_file_fb = 'twitt.csv'
        csv_file_path = os.path.join(current_directory, csv_file_fb)

        # Open the CSV file and read its content
        with open(csv_file_path, 'r') as csv_file:
            # Use DictReader to read CSV data into a list of dictionaries
            csv_reader = csv.DictReader(csv_file)
            data = [row for row in csv_reader]

        text_dict = {"reviews": data}
        print("text_dict:", text_dict["reviews"])
        # Convert the list of dictionaries to a JSON array
        # json_data = json.dumps(text_dict, indent=2)

        reviews = []

        for item in text_dict["reviews"]:
            # print("item :",item)
            reviews.append(item["review"])
        finalText = reviews

        store_twitter_data(
            request,
            data={
                'sentiment': result,
                'text': finalText,
                'reviewsRatio': {},
                'totalReviews': 1,
                'showReviewsRatio': False
            }
        )

        return render(
            request,
            'realworld/results.html',
            {
                'sentiment': result,
                'text': finalText,
                'reviewsRatio': {},
                'totalReviews': 1,
                'showReviewsRatio': False
            }
        )
    else:
        note = "Please Enter the product blog link for analysis"
        return render(
            request,
            'realworld/productanalysis.html',
            {'note': note}
        )


def redditanalysis(request):
    if request.method == 'POST':
        blogname = request.POST.get("blogname", "")
        # Get the Reddit post URL from the form
        fetched_data = fetch_reddit_post(blogname)
        # Fetch the Reddit post details

        # Combine the fetched data (title, body, comments)
        # into a single list for analysis
        data = [
            fetched_data["title"],
            fetched_data["body"]
        ] + fetched_data["comments"]
        # Perform sentiment analysis
        result = reddit_sentiment_score(data)

        # Combine the title, body, and comments into a single
        # list for displaying on the results page
        reviews = [
            f"Title: {fetched_data['title']}",
            f"Body: {fetched_data['body']}"
        ] + fetched_data["comments"]

        store_reddit_data(
            request,
            data={
                'sentiment': result,
                'text': reviews,
                'reviewsRatio': {},
                'totalReviews': len(reviews),
                'showReviewsRatio': False
            }
        )

        return render(request, 'realworld/results.html', {
            'sentiment': result,  # Sentiment analysis result
            'text': reviews,  # Display the text analyzed
            'reviewsRatio': {},  # Placeholder
            'totalReviews': len(reviews),  # Total number of items analyzed
            'showReviewsRatio': False
        })
    else:
        note = "Enter the Reddit post URL for analysis"
        return render(request, 'realworld/redditanalysis.html', {'note': note})


def audioanalysis(request):
    if request.method == 'POST':
        file = request.FILES['audioFile']
        fs = FileSystemStorage()
        fs.save(file.name, file)
        pathname = "sentimental_analysis/media/"
        extension_name = file.name
        extension_name = extension_name[len(extension_name) - 3:]
        path = pathname + file.name
        result = {}
        destination_folder = 'sentimental_analysis/media/audio/'
        shutil.copy(path, destination_folder)
        useFile = destination_folder + file.name
        text = speech_to_text(useFile)
        finalText = text
        result = detailed_analysis(text)

        folder_path = 'sentimental_analysis/media/'
        files = os.listdir(folder_path)
        for file in files:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        store_audio_analysis(
            request,
            data={
                'sentiment': result,
                'text': finalText,
                'reviewsRatio': {},
                'totalReviews': 1,
                'showReviewsRatio': False
            }
        )
        return render(
            request,
            'realworld/results.html',
            {
                'sentiment': result,
                'text': finalText,
                'reviewsRatio': {},
                'totalReviews': 1,
                'showReviewsRatio': False
            }
        )
    else:
        note = "Please Enter the audio file you want to analyze"
        return render(request, 'realworld/audio.html', {'note': note})


def livespeechanalysis(request):
    if request.method == 'POST':
        my_file_handle = open(
            'sentimental_analysis/realworld/recordedAudio.txt')
        audioFile = my_file_handle.read()
        result = {}
        text = speech_to_text(audioFile)

        finalText = text
        result = detailed_analysis(text)
        folder_path = 'sentimental_analysis/media/recordedAudio/'
        files = os.listdir(folder_path)
        for file in files:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        store_live_analysis(
            request,
            data={
                'sentiment': result,
                'text': finalText,
                'reviewsRatio': {},
                'totalReviews': 1,
                'showReviewsRatio': False
            }
        )
        return render(
            request,
            'realworld/results.html',
            {
                'sentiment': result,
                'text': finalText,
                'reviewsRatio': {},
                'totalReviews': 1,
                'showReviewsRatio': False
            }
        )


@csrf_exempt
def recordaudio(request):
    if request.method == 'POST':
        audio_file = request.FILES['liveaudioFile']
        fs = FileSystemStorage()
        fs.save(audio_file.name, audio_file)
        folder_path = 'sentimental_analysis/media/'
        files = os.listdir(folder_path)

        pathname = "sentimental_analysis/media/"
        extension_name = audio_file.name
        extension_name = extension_name[len(extension_name) - 3:]
        path = pathname + audio_file.name
        audioName = audio_file.name
        destination_folder = 'sentimental_analysis/media/recordedAudio/'
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        shutil.copy(path, destination_folder)
        useFile = destination_folder + audioName
        for file in files:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        audio = AudioSegment.from_file(useFile)
        audio = audio.set_sample_width(2)
        audio = audio.set_frame_rate(44100)
        audio = audio.set_channels(1)
        audio.export(useFile, format='wav')

        text_file_path = "sentimental_analysis/realworld/recordedAudio.txt"
        with open(text_file_path, "w") as text_file:
            text_file.write(useFile)

        response = HttpResponse(
            'Success! This is a 200 response.',
            content_type='text/plain',
            status=200
        )
        return response


analysis_cache = AnalysisCache()


def newsanalysis(request):
    if request.method == 'POST':
        topicname = request.POST.get("topicname", "")
        scrapNews(topicname, 10)

        f = r'sentimental_analysis/realworld/news.json'
        with open(f, 'r') as json_file:
            json_data = json.load(json_file)
        news = []
        for item in json_data:
            news.append(item['Summary'])

        cached_sentiment, cached_text = analysis_cache.get_analysis(topicname,
                                                                    news
                                                                    )

        if cached_sentiment and cached_text:
            print('loaded sentiment')
            return render(request, 'realworld/results.html', {
                'sentiment': cached_sentiment,
                'text': cached_text,
                'reviewsRatio': {},
                'totalReviews': 1,
                'showReviewsRatio': False
            })

        finalText = news
        result = detailed_analysis(news)
        print('cached sentiment')
        analysis_cache.set_analysis(topicname, news, result, finalText)

        store_news_analysis(
            request,
            data={
                'sentiment': result,
                'text': finalText,
                'reviewsRatio': {},
                'totalReviews': 1,
                'showReviewsRatio': False
            }
        )

        return render(request, 'realworld/results.html', {
            'sentiment': result,
            'text': finalText,
            'reviewsRatio': {},
            'totalReviews': 1,
            'showReviewsRatio': False
        })

    else:
        return render(request, 'realworld/index.html')


def speech_to_text(filename):
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        return text


def sentiment_analyzer_scores(sentence):
    analyser = SentimentIntensityAnalyzer()
    score = analyser.polarity_scores(sentence)
    return score


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key, 0)


@login_required
def text_history_detail(request, timestamp):
    user = get_user(request)
    username = user.username

    # Define the directory path
    directory_path = os.path.join(
        "sentimental_analysis",
        "media",
        "user_data"
    )
    file_path = os.path.join(directory_path, f"{username}.json")

    history_data = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            history_data = json.load(json_file)

    # Find the specific analysis data by timestamp
    analysis_data = history_data.get('Text_Analysis', {}).get(timestamp)

    if analysis_data is None:
        return HttpResponse("Analysis data not found", status=404)

    return render(
        request,
        'realworld/results.html',
        {
            'sentiment': analysis_data['sentiment'],
            'text': analysis_data['text'],
            'reviewsRatio': analysis_data.get('reviewsRatio', {}),
            'totalReviews': analysis_data.get('totalReviews', 1),
            'showReviewsRatio': analysis_data.get('showReviewsRatio', False)
        }
    )


@login_required
def image_history_detail(request, timestamp):
    user = get_user(request)
    username = user.username

    # Define the directory path
    directory_path = os.path.join(
        "sentimental_analysis",
        "media",
        "user_data"
    )
    file_path = os.path.join(directory_path, f"{username}.json")

    history_data = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            history_data = json.load(json_file)

    # Find the specific analysis data by timestamp
    analysis_data = history_data.get('Image_Analysis', {}).get(timestamp)

    if analysis_data is None:
        return HttpResponse("Analysis data not found for image", status=404)

    return render(
            request,
            'realworld/resultsimage.html',
            {
                'sentiment': analysis_data['sentiment'],
                'text': analysis_data['text'],
                'analyzed_image_path': analysis_data['analyzed_image_path']
            }
        )


def news_history_detail(request, timestamp):
    user = get_user(request)
    username = user.username

    # Define the directory path
    directory_path = os.path.join(
        "sentimental_analysis",
        "media",
        "user_data"
    )
    file_path = os.path.join(directory_path, f"{username}.json")

    history_data = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            history_data = json.load(json_file)

    # Find the specific analysis data by timestamp
    analysis_data = history_data.get('News_Analysis', {}).get(timestamp)

    if analysis_data is None:
        return HttpResponse("Analysis data not found for news", status=404)

    return render(
        request,
        'realworld/results.html',
        {
            'sentiment': analysis_data['sentiment'],
            'text': analysis_data['text'],
            'reviewsRatio': analysis_data.get('reviewsRatio', {}),
            'totalReviews': analysis_data.get('totalReviews', 1),
            'showReviewsRatio': analysis_data.get('showReviewsRatio', False)
        }
    )


def document_history_detail(request, timestamp):
    user = get_user(request)
    username = user.username

    # Define the directory path
    directory_path = os.path.join(
        "sentimental_analysis",
        "media",
        "user_data"
    )
    file_path = os.path.join(directory_path, f"{username}.json")

    history_data = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            history_data = json.load(json_file)

    # Find the specific analysis data by timestamp
    analysis_data = history_data.get('Doc_Analysis', {}).get(timestamp)

    if analysis_data is None:
        return HttpResponse("Analysis data not found for document", status=404)

    return render(
        request,
        'realworld/results.html',
        {
            'sentiment': analysis_data['sentiment'],
            'text': analysis_data['text'],
            'reviewsRatio': analysis_data.get('reviewsRatio', {}),
            'totalReviews': analysis_data.get('totalReviews', 1),
            'showReviewsRatio': analysis_data.get('showReviewsRatio', False)
        }
    )


def audio_history_detail(request, timestamp):
    user = get_user(request)
    username = user.username

    # Define the directory path
    directory_path = os.path.join(
        "sentimental_analysis",
        "media",
        "user_data"
    )
    file_path = os.path.join(directory_path, f"{username}.json")

    history_data = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            history_data = json.load(json_file)

    # Find the specific analysis data by timestamp
    analysis_data = history_data.get('Audio_Analysis', {}).get(timestamp)

    if analysis_data is None:
        return HttpResponse("Analysis data not found for audio", status=404)

    return render(
            request,
            'realworld/results.html',
            {
                'sentiment': analysis_data['sentiment'],
                'text': analysis_data['text'],
                'reviewsRatio': analysis_data.get('reviewsRatio', {}),
                'totalReviews': analysis_data.get('totalReviews', 1),
                'showReviewsRatio': analysis_data.get(
                    'showReviewsRatio',
                    False
                )
            }
        )


def live_history_detail(request, timestamp):
    user = get_user(request)
    username = user.username

    # Define the directory path
    directory_path = os.path.join(
        "sentimental_analysis",
        "media",
        "user_data"
    )
    file_path = os.path.join(directory_path, f"{username}.json")

    history_data = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            history_data = json.load(json_file)

    # Find the specific analysis data by timestamp
    analysis_data = history_data.get('Live_Speech', {}).get(timestamp)

    if analysis_data is None:
        return HttpResponse(
            "Analysis data not found for live speech",
            status=404
        )

    return render(
            request,
            'realworld/results.html',
            {
                'sentiment': analysis_data['sentiment'],
                'text': analysis_data['text'],
                'reviewsRatio': analysis_data.get('reviewsRatio', {}),
                'totalReviews': analysis_data.get('totalReviews', 1),
                'showReviewsRatio': analysis_data.get(
                    'showReviewsRatio',
                    False
                )
            }
        )


def reddit_history_detail(request, timestamp):
    user = get_user(request)
    username = user.username

    # Define the directory path
    directory_path = os.path.join(
        "sentimental_analysis",
        "media",
        "user_data"
    )
    file_path = os.path.join(directory_path, f"{username}.json")

    history_data = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            history_data = json.load(json_file)

    # Find the specific analysis data by timestamp
    analysis_data = history_data.get('Reddit', {}).get(timestamp)

    if analysis_data is None:
        return HttpResponse("Analysis data not found for Reddit", status=404)

    return render(
        request,
        'realworld/results.html',
        {
            'sentiment': analysis_data['sentiment'],
            'text': analysis_data['text'],
            'reviewsRatio': analysis_data.get('reviewsRatio', {}),
            'totalReviews': analysis_data.get('totalReviews', 1),
            'showReviewsRatio': analysis_data.get('showReviewsRatio', False)
        }
    )

def youtube_history_detail(request, timestamp):
    user = get_user(request)
    username = user.username

    # Define the directory path
    directory_path = os.path.join(
        "sentimental_analysis",
        "media",
        "user_data"
    )
    file_path = os.path.join(directory_path, f"{username}.json")

    history_data = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            history_data = json.load(json_file)

    # Find the specific analysis data by timestamp
    analysis_data = history_data.get('Youtube', {}).get(timestamp)

    if analysis_data is None:
        return HttpResponse("Analysis data not found for Youtube", status=404)

    return render(
        request,
        'realworld/results.html',
        {
            'sentiment': analysis_data['sentiment'],
            'text': analysis_data['text'],
            'reviewsRatio': analysis_data.get('reviewsRatio', {}),
            'totalReviews': analysis_data.get('totalReviews', 1),
            'showReviewsRatio': analysis_data.get('showReviewsRatio', False)
        }
    )


def twitter_history_detail(request, timestamp):
    user = get_user(request)
    username = user.username

    # Define the directory path
    directory_path = os.path.join(
        "sentimental_analysis",
        "media",
        "user_data"
    )
    file_path = os.path.join(directory_path, f"{username}.json")

    history_data = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            history_data = json.load(json_file)

    # Find the specific analysis data by timestamp
    analysis_data = history_data.get('Twitter', {}).get(timestamp)

    if analysis_data is None:
        return HttpResponse(
            "Analysis data not found for Twitter",
            status=404
        )

    return render(
        request,
        'realworld/results.html',
        {
            'sentiment': analysis_data['sentiment'],
            'text': analysis_data['text'],
            'reviewsRatio': analysis_data.get('reviewsRatio', {}),
            'totalReviews': analysis_data.get('totalReviews', 1),
            'showReviewsRatio': analysis_data.get('showReviewsRatio', False)
        }
    )


def facebook_history_detail(request, timestamp):
    user = get_user(request)
    username = user.username

    # Define the directory path
    directory_path = os.path.join(
        "sentimental_analysis",
        "media",
        "user_data"
    )
    file_path = os.path.join(directory_path, f"{username}.json")

    history_data = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            history_data = json.load(json_file)

    # Find the specific analysis data by timestamp
    analysis_data = history_data.get('Facebook', {}).get(timestamp)

    if analysis_data is None:
        return HttpResponse(
            "Analysis data not found for Facebook",
            status=404
        )

    return render(
        request,
        'realworld/results.html',
        {
            'sentiment': analysis_data['sentiment'],
            'text': analysis_data['text'],
            'reviewsRatio': analysis_data.get('reviewsRatio', {}),
            'totalReviews': analysis_data.get('totalReviews', 1),
            'showReviewsRatio': analysis_data.get('showReviewsRatio', False)
        }
    )


def product_history_detail(request, timestamp):
    user = get_user(request)
    username = user.username

    # Define the directory path
    directory_path = os.path.join(
        "sentimental_analysis",
        "media",
        "user_data"
    )
    file_path = os.path.join(directory_path, f"{username}.json")

    history_data = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            history_data = json.load(json_file)

    # Find the specific analysis data by timestamp
    analysis_data = history_data.get('Product_Analysis', {}).get(timestamp)

    if analysis_data is None:
        return HttpResponse(
            "Analysis data not found for product",
            status=404
        )

    return render(
        request,
        'realworld/results.html',
        {
            'sentiment': analysis_data['sentiment'],
            'text': analysis_data['text'],
            'reviewsRatio': analysis_data.get('reviewsRatio', {}),
            'totalReviews': analysis_data.get('totalReviews', 1),
            'showReviewsRatio': analysis_data.get('showReviewsRatio', False)
        }
    )


def privacy_policy(request):
    return render(request, 'realworld/privacy_policy.html')
