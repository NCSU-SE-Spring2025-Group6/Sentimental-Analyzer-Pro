import unittest
import os, sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
# from views import detailed_analysis_sentence
from sentimental_analysis.realworld.views import detailed_analysis_sentence
class TestViews(unittest.TestCase):
    
    def test_detailed_analysis_sentence_negative_sentence(self):
        response = detailed_analysis_sentence("""I can't express how disappointed I am with the SuperClean 3000. Right out of the box, it felt cheap and flimsy. The suction is practically nonexistent—I've had better results using a broom! It barely picked up anything, leaving behind dirt and pet hair everywhere.

The design is another nightmare. It's so heavy and awkward that I dreaded using it. And don't get me started on the attachments; they just fell off at the worst times, making the whole experience even more frustrating.

After only a few uses, it started making a terrible grinding noise. I reached out to customer service, and it was a total waste of time. I was put on hold for ages, and when I finally got through, they were of no help at all.

Honestly, I regret purchasing this vacuum. Save your money and look for something else!""")
        self.assertLess(response['compound'], -0.4)

    def test_detailed_analysis_sentence_neutral_sentence(self):
        response = detailed_analysis_sentence("""The SuperClean 3000 vacuum is a functional product that meets basic cleaning needs. It picks up dust and small debris, although its suction power could be improved. The design is somewhat bulky, which may affect maneuverability in tighter spaces.

The included attachments work as intended, but they are fairly standard and do not offer any unique features. Overall, it performs adequately for everyday use, but it might not be the best option for those seeking advanced cleaning capabilities.""")
        self.assertGreater(response['compound'], -0.4)
        self.assertLess(response['compound'], 0.4)

    def test_detailed_analysis_sentence_positive_sentence(self):
        response = detailed_analysis_sentence("""\n\n\n\n\n\n\n\n\n\n  \n  \n    \n  These Palazzo Pants are GORGEOUS! The material IS very light and slightly see through, as others have mentioned, however if you wear a pair of nude colored undies it won't pose a problem :-) I am 5'4\" and about 190lbs. I normally wear a size 12/14- Large pant and I got these in an XL and they fit me VERY comfortably. In my opinion, get 1 size up for adequate comfort and you will NOT be disappointed. I have received lots of compliments on these and people actually think it is a skirt :-P I'm super cheap and almost died after I paid the $38 for these but I am happy I did because I really do like them a lot :-) I paired them with a dark green top, also from Amazon, called the LL Womens Boat Neck Dolman Top, for $12.95 and they work wonderfully together! Both are super flowey and comfy. Bring on the warm weather!!! :-D\n\n  \n""")
        self.assertGreater(response['compound'], 0.4)
if __name__ == '__main__':
    unittest.main()