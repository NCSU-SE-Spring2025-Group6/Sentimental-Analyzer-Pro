"""sentimental_analysis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path, include
from django.conf import settings
from django.conf.urls.static import static
import realworld.views  # Import views from the realworld app
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path('auth/', include('authapp.urls')),
    re_path('auth/login/', auth_views.LoginView.as_view(), name='login'),
    re_path(
        'auth/logout/',
        auth_views.LogoutView.as_view(next_page='login'),
        name='logout'
    ),
    re_path(r'^$', realworld.views.analysis, name='analysis'),
    re_path(r'^inputimage', realworld.views.inputimage, name='inputimage'),
    re_path(r'^input', realworld.views.input, name='input'),
    re_path(
        r'^productanalysis',
        realworld.views.productanalysis,
        name='product analysis'
    ),
    re_path(
        r'^textanalysis',
        realworld.views.textanalysis,
        name='text analysis'
    ),
    re_path(
        r'^audioanalysis',
        realworld.views.audioanalysis,
        name='audio analysis'
    ),
    re_path(
        r'^livespeechanalysis',
        realworld.views.livespeechanalysis,
        name='live speech analysis'
    ),
    re_path(
        r'^fbanalysis',
        realworld.views.fbanalysis,
        name='fb analysis'
    ),
    re_path(
        r'^twitteranalysis',
        realworld.views.twitteranalysis,
        name='twitter analysis'
    ),
    re_path(
        r'^redditanalysis',
        realworld.views.redditanalysis,
        name='reddit analysis'
    ),
    re_path(
        r'^youtubetranscriptanalysis',
        realworld.views.youtube_transcript_analysis,
        name='youtube transcript analysis'
    ),
    re_path(
        r'^youtubecommentsanalysis',
        realworld.views.youtube_comments_analysis,
        name='youtube comments analysis'
    ),
    re_path(
        r'^recordAudio',
        realworld.views.recordaudio,
        name='recordAudio'
    ),
    re_path(
        r'^newsanalysis',
        realworld.views.newsanalysis,
        name='news analysis'
    ),
    re_path(
        r'^batch_analysis',
        realworld.views.batch_analysis,
        name='batch_text_analysis'
    ),
    path(
        'profile/',
        realworld.views.profile_view,
        name='profile'
    ),
    path(
        'history/',
        realworld.views.history_view,
        name='history'
    ),
    path(
        'delete-history-entry/', 
        realworld.views.delete_history_entry,
        name='delete_history_entry'
    ),
    path(
        'settings/',
        realworld.views.settings_view,
        name='settings'
    ),
    path(
        'update_profile/',
        realworld.views.update_profile,
        name='update_profile'
    ),
    path(
        'update_account/',
        realworld.views.update_account,
        name='update_account'
    ),
    path(
        'opt_out/',
        realworld.views.opt_out,
        name='opt_out'
    ),
    path(
        'delete_data',
        realworld.views.delete_data,
        name='delete_data'
    ),
    path(
        'history/text/<str:timestamp>/',
        realworld.views.text_history_detail,
        name='text_history_detail'),
    path(
        'history/image/<str:timestamp>/',
        realworld.views.image_history_detail,
        name='image_history_detail'),
    path(
        'history/news/<str:timestamp>/',
        realworld.views.news_history_detail,
        name='news_history_detail'),
    path(
        'history/document/<str:timestamp>/',
        realworld.views.document_history_detail,
        name='document_history_detail'),
    path(
        'history/audio/<str:timestamp>/',
        realworld.views.audio_history_detail,
        name='audio_history_detail'),
    path(
        'history/live/<str:timestamp>/',
        realworld.views.live_history_detail,
        name='live_history_detail'),
    path(
        'history/reddit/<str:timestamp>/',
        realworld.views.reddit_history_detail,
        name='reddit_history_detail'),
    path(
        'history/youtube/<str:timestamp>/',
        realworld.views.youtube_history_detail,
        name='youtube_history_detail'),
    path(
        'history/twitter/<str:timestamp>/',
        realworld.views.twitter_history_detail,
        name='twitter_history_detail'),
    path(
        'history/facebook/<str:timestamp>/',
        realworld.views.facebook_history_detail,
        name='facebook_history_detail'),
    path(
        'history/product/<str:timestamp>/',
        realworld.views.product_history_detail,
        name='product_history_detail'),
    path(
        'privacy-policy/',
        realworld.views.privacy_policy,
        name='privacy_policy'
    ),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
