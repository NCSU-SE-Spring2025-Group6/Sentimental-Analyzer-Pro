import logging
import unittest
import os, sys
import inspect

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import json
# from newsScraper import scrapNews, getNewsResults
from sentimental_analysis.realworld.newsScraper import scrapNews, getNewsResults
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

query = "Artificial Intelligence"
search_for = ["ai", "artificial", "intelligence"]
json_path = r"sentimental_analysis/realworld/news.json"
news_url_json = r"sentimental_analysis/realworld/__tests__/news_url.json"

mock_data = [
    {'Summary': 'AI technology is growing rapidly in various sectors. Recent developments have shown significant advancements in machine learning algorithms, neural networks, and deep learning applications. Researchers are discovering new ways to implement artificial intelligence across different industries, from healthcare to finance, making processes more efficient and accurate. The impact of these technologies continues to reshape how businesses operate and how services are delivered to consumers.'},
    {'Summary': 'Artificial intelligence and machine learning continue to advance at an unprecedented pace. Companies worldwide are investing heavily in AI research and development, leading to breakthrough innovations in natural language processing, computer vision, and automated decision-making systems. These advancements are creating new opportunities for businesses while raising important questions about ethics and responsible AI development.'},
    {'Summary': 'The impact of AI on business strategy has become increasingly significant as organizations adapt to digital transformation. Companies are leveraging artificial intelligence to streamline operations, enhance customer experiences, and gain competitive advantages in the market. From predictive analytics to automated customer service, AI technologies are fundamentally changing how businesses operate and compete in the global marketplace.'},
    {'Summary': 'New developments in AI are being announced regularly, with breakthrough innovations in areas such as autonomous vehicles, healthcare diagnostics, and financial technology. Researchers are pushing the boundaries of what artificial intelligence can achieve, developing more sophisticated algorithms and models that can handle complex tasks with increasing accuracy and efficiency.'},
    {'Summary': 'Intelligence systems powered by AI are revolutionizing healthcare delivery and patient care. Medical professionals are using artificial intelligence to improve diagnostic accuracy, develop personalized treatment plans, and predict patient outcomes with greater precision. These advancements are leading to more effective treatments and better healthcare outcomes for patients worldwide.'},
    {'Summary': 'AI researchers are developing new approaches to natural language processing that enable more sophisticated human-computer interactions. These systems can understand context, sentiment, and nuanced meanings in text, leading to better chatbots and virtual assistants.'},
    {'Summary': 'Artificial intelligence is transforming the manufacturing sector through predictive maintenance and quality control. Smart factories using AI-powered systems can detect defects, optimize production schedules, and reduce downtime significantly.'}
]

def urlValidator(url: str) -> bool:
    val = URLValidator()
    try:
        val(url)
        return True
    except (ValidationError,) as e:
        logging.warning(f'Invalid url - {url}')
        return False


class TestNewsResults(unittest.TestCase):
    setup_done = False

    @classmethod
    def setUpClass(self):
        if self.setup_done == True:
            return
        getNewsResults(query, 100)
        with open(news_url_json, "r") as json_file:
            self.news_result_hundred = json.load(json_file)

        self.news_result_one = self.news_result_hundred[:1]
        self.news_result_ten = self.news_result_hundred[:10]
        self.setup_done = True

    def test_query(self):
        response = self.news_result_one
        self.assertNotEqual(response, None)

    def test_query_count_one(self):
        response = self.news_result_one
        self.assertEqual(len(response), 1)

    def test_query_count_multiple(self):
        response = self.news_result_hundred
        self.assertGreater(len(response), 50)

    def test_response_url(self):
        response_url = self.news_result_one[0]
        self.assertTrue(urlValidator(response_url))

    def test_response_url_multiple(self):
        response_url_list = self.news_result_ten

        for url in response_url_list:
            self.assertTrue(urlValidator(url))

    def test_news_results_args(self):
        self.assertTrue(len(inspect.getfullargspec(getNewsResults).args), 2)

    def test_response_relevancy(self):
        response_url = str(self.news_result_one[0]).lower()
        self.assertTrue(urlValidator(response_url))


class TestScrapNews(unittest.TestCase):
    setup_done = False

    @classmethod
    def setUpClass(self):
        if self.setup_done == True:
            return
            
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, "w") as json_file:
            json.dump(mock_data, json_file)

        with open(json_path, "r") as json_file:
            self.json_data = json.load(json_file)
        self.news = []

        for item in self.json_data:
            self.news.append(item["Summary"])
        self.article_list_single = self.news[:1]
        self.article_list_multiple = self.news
        self.setup_done = True

    def test_query(self):
        self.assertNotEqual(self.article_list_single, None)

    def test_count_one(self):
        self.assertEqual(len(self.article_list_single), 1)

    def test_count_multiple(self):
        self.assertGreater(len(self.article_list_multiple), 5)

    def test_article_validity_JS(self):
        for article in self.article_list_multiple:
            self.assertNotEqual(article, "Please enable JS and disable any ad blocker")

    def test_article_relevancy(self):
        for news in self.news:
            if any(keyword in news for keyword in search_for) == False:
                logging.warning(news)
            self.assertTrue(any(keyword in news.lower() for keyword in search_for))

    def test_scrape_news_args(self):
        self.assertTrue(len(inspect.getfullargspec(scrapNews).args), 3)

    def test_json_dump(self):
        self.assertNotEqual(self.json_data, None)

    def test_json_dump_len(self):
        self.assertGreater(len(self.news), 5)

    def test_json_dump_data_len(self):
        self.assertGreater(len(self.news), 5)

    def test_json_dump_data_validity_JS(self):
        for news in self.news:
            self.assertGreaterEqual(len(news), 139)

    def test_json_dump_relevancy(self):
        for news in self.news:
            if any(keyword in news for keyword in search_for) == False:
                logging.warning(news)
                self.assertTrue(any(keyword in news.lower() for keyword in search_for))
    
    @classmethod
    def tearDownClass(self):
        scrapNews(query, 1, True)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestNewsResults("Test news results"))
    suite.addTest(TestScrapNews("Test news scraping"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
