"""
URL configuration for orda_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# Жаңа функцияларды импорттауды тексеріңіз:
from core.views import index, about, games_home, game_quiz, game_match, game_picture 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('about/', about, name='about'),               # Біз туралы
    path('games/', games_home, name='games'),          # Ойындар тізімі

    # Ойын логикасы мен нәтижелері бірдей URL-мен өтеді (GET және POST)
    path('games/quiz/', game_quiz, name='quiz'),       # 1. Тест
    path('games/match/', game_match, name='match'),    # 2. Сәйкестендіру
    path('games/picture/', game_picture, name='picture'), # 3. Сурет

    # Нәтижелер бетіне арналған жеке URL қажет емес, себебі нәтижелер 'quiz' және 'match' URL-дарындағы POST арқылы өңделеді.
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)