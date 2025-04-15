from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
import os

def extract_video_id(url):
    """Extracts the YouTube video ID from a YouTube URL."""
    parsed_url = urlparse(url)

    if parsed_url.netloc in ['www.youtube.com', 'm.youtube.com']:
        query_params = parse_qs(parsed_url.query)
        video_id_list = query_params.get('v')
        if video_id_list:
            return video_id_list[0]
    elif parsed_url.netloc == 'youtu.be':
        return parsed_url.path[1:]  # Remove the leading '/'

    return None

def get_transcript(video_link):

    video_id = extract_video_id(video_link)

    try:
        ytt_api = YouTubeTranscriptApi()
        transcription = ytt_api.fetch(video_id=video_id)
        transcript_text = ' '.join([snippet.text for snippet in transcription])
        return transcript_text
    except:
        print('Error getting transcription')
        return None

def get_top_liked_comments(video_link, max_results=10):

    video_id = extract_video_id(video_link)
    API_KEY = os.environ.get('YOUTUBE_API_KEY')
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

    try:
        comments_request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=max_results,
            order='relevance',  # While 'relevance' is default, we'll sort later
            textFormat='plainText'
        )
        comments_response = comments_request.execute()
        comment_data = []

        for item in comments_response.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']
            comment_data.append({
                'text': comment['textDisplay'],
                'likes': comment['likeCount']
            })

        # Sort comments by like count in descending order
        sorted_comments = sorted(comment_data, key=lambda x: x['likes'], reverse=True)
        comments = [item['text'] for item in sorted_comments]

        return '. '.join(comments[:max_results])  # Ensure we only return up to max_results

    except Exception as e:
        print(f'An error occurred: {e}')
        return None
