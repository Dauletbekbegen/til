from django.shortcuts import render
from .models import CorpusEntry, Author, Work, Category, GameImage
from django.db.models import Q
import random

# 1. БАСТЫ БЕТ (Іздеу)
def index(request):
    authors = Author.objects.all()
    works = Work.objects.all()
    categories = Category.objects.all()
    results = None
    query = request.GET.get('q')
    selected_author = request.GET.get('author')
    selected_work = request.GET.get('work')
    selected_categories = request.GET.getlist('category')

    if query or selected_categories or (selected_author and selected_author != 'all') or (selected_work and selected_work != 'all'):
        results = CorpusEntry.objects.all()
        if query:
            results = results.filter(Q(entry_title__icontains=query) | Q(meaning__icontains=query) | Q(example_text__icontains=query))
        if selected_author and selected_author != 'all':
            results = results.filter(work__author_id=selected_author)
        if selected_work and selected_work != 'all':
            results = results.filter(work_id=selected_work)
        if selected_categories:
            results = results.filter(category__id__in=selected_categories)

    context = {
        'authors': authors, 'works': works, 'categories': categories,
        'results': results, 'query': query, 'selected_categories': selected_categories
    }
    return render(request, 'index.html', context)

# 2. БІЗ ТУРАЛЫ
def about(request):
    return render(request, 'about.html')

# 3. ОЙЫНДАР БЕТІ
def games_home(request):
    return render(request, 'games.html')

# ... (басқа импорттар мен функциялар)

# ОЙЫН 1: ТЕСТ (Quiz)
def game_quiz(request):
    works = Work.objects.all()

    # ЕГЕР ФОРМАДАН ЖАУАПТАР КЕЛСЕ (Ойын аяқталса)
    if request.method == 'POST':
        user_answers = {}
        for key, value in request.POST.items():
            if key.startswith('q_'):
                # Формат: {'q_123': 'Дұрыс жауап мәтіні'}
                user_answers[key.split('_')[1]] = value 
        
        # Деректерді базадан алып, нәтижелерді есептеу
        results = []
        correct_count = 0
        total_questions = len(user_answers)
        
        entry_ids = user_answers.keys()
        entries = CorpusEntry.objects.filter(id__in=entry_ids)
        
        for entry in entries:
            user_answer = user_answers.get(str(entry.id))
            is_correct = (entry.meaning.strip().lower() == user_answer.strip().lower())
            
            if is_correct:
                correct_count += 1
            
            results.append({
                'id': entry.id,
                'question': entry.entry_title,
                'correct_answer': entry.meaning,
                'user_answer': user_answer,
                'is_correct': is_correct,
            })
            
        context = {
            'results': results,
            'correct_count': correct_count,
            'total_questions': total_questions
        }
        # Нәтижелер бетіне жібереміз
        return render(request, 'game_quiz_results.html', context)

    # ЕГЕР ОЙЫН БАСТАЛСА (GET сұранысы)
    if request.GET.get('start_game'):
        work_id = request.GET.get('work')
        count = int(request.GET.get('count', 5))
        
        entries = CorpusEntry.objects.filter(meaning__isnull=False).exclude(meaning__exact='')
        if work_id and work_id != 'all':
            entries = entries.filter(work_id=work_id)
        
        entries = list(entries)
        random.shuffle(entries)
        entries = entries[:count]
        
        quiz_data = []
        all_answers = [e.meaning for e in CorpusEntry.objects.all() if e.meaning]

        for item in entries:
            # 3 қате жауап таңдау
            distractors = random.sample(all_answers, 3) if len(all_answers) >= 3 else all_answers
            options = list(set(distractors + [item.meaning])) # Қайталанбау үшін
            random.shuffle(options)
            
            quiz_data.append({
                'id': item.id, # Жауапты өңдеу үшін ID қажет
                'question': item.entry_title,
                'options': options,
                'correct_answer': item.meaning
            })
            
        return render(request, 'game_quiz_play.html', {'quiz_data': quiz_data})

    return render(request, 'game_quiz_setup.html', {'works': works})


# ОЙЫН 2: СӘЙКЕСТЕНДІРУ
def game_match(request):
    if request.GET.get('start_game'):
        count = int(request.GET.get('count', 5))
        entries = list(CorpusEntry.objects.filter(meaning__isnull=False)[:50]) # Соңғы 50 сөзден аламыз
        random.shuffle(entries)
        selected = entries[:count]
        
        # Сөздер мен мағыналарды бөлек жібереміз (араластырып)
        words = [{'id': x.id, 'text': x.entry_title} for x in selected]
        meanings = [{'id': x.id, 'text': x.meaning} for x in selected]
        random.shuffle(meanings)
        
        return render(request, 'game_match_play.html', {'words': words, 'meanings': meanings, 'count': count})
        
    return render(request, 'game_match_setup.html')

# ОЙЫН 3: СУРЕТ
def game_picture(request):
    if request.GET.get('start_game'):
        count = int(request.GET.get('count', 5))
        images = list(GameImage.objects.all())
        random.shuffle(images)
        images = images[:count]
        
        return render(request, 'game_picture_play.html', {'images': images})
        
    return render(request, 'game_picture_setup.html')