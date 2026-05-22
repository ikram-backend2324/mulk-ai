from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings
import requests
import json

from .models import Property, PropertyImage, Favorite, UserProfile
from .forms import PropertyForm, RegisterForm, PropertyImageFormSet


def home(request):
    featured = Property.objects.filter(is_active=True, is_featured=True)[:6]
    recent = Property.objects.filter(is_active=True)[:8]
    total_props = Property.objects.filter(is_active=True).count()
    cities = Property.objects.filter(is_active=True).values_list('city', flat=True).distinct()
    context = {
        'featured': featured,
        'recent': recent,
        'total_props': total_props,
        'cities_count': cities.count(),
    }
    return render(request, 'properties/home.html', context)


def property_list(request):
    qs = Property.objects.filter(is_active=True)
    listing_type = request.GET.get('listing_type', '')
    property_type = request.GET.get('property_type', '')
    city = request.GET.get('city', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    min_area = request.GET.get('min_area', '')
    max_area = request.GET.get('max_area', '')
    sort = request.GET.get('sort', '-created_at')
    q = request.GET.get('q', '')

    if listing_type:
        qs = qs.filter(listing_type=listing_type)
    if property_type:
        qs = qs.filter(property_type=property_type)
    if city:
        qs = qs.filter(city__icontains=city)
    if min_price:
        qs = qs.filter(price__gte=min_price)
    if max_price:
        qs = qs.filter(price__lte=max_price)
    if min_area:
        qs = qs.filter(area__gte=min_area)
    if max_area:
        qs = qs.filter(area__lte=max_area)
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(city__icontains=q))

    sort_map = {
        '-created_at': '-created_at',
        'price_asc': 'price',
        'price_desc': '-price',
    }
    qs = qs.order_by(sort_map.get(sort, '-created_at'))

    all_cities = Property.objects.filter(is_active=True).values_list('city', flat=True).distinct()

    context = {
        'properties': qs,
        'listing_type': listing_type,
        'property_type': property_type,
        'city': city,
        'min_price': min_price,
        'max_price': max_price,
        'min_area': min_area,
        'max_area': max_area,
        'sort': sort,
        'q': q,
        'all_cities': all_cities,
    }
    return render(request, 'properties/list.html', context)


def property_detail(request, pk):
    prop = get_object_or_404(Property, pk=pk, is_active=True)
    similar = Property.objects.filter(
        is_active=True,
        property_type=prop.property_type,
        listing_type=prop.listing_type
    ).exclude(pk=pk)[:4]
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, property=prop).exists()
    context = {
        'prop': prop,
        'similar': similar,
        'is_favorite': is_favorite,
    }
    return render(request, 'properties/detail.html', context)


@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.owner = request.user
            prop.save()
            images = request.FILES.getlist('images')
            for i, img in enumerate(images):
                PropertyImage.objects.create(property=prop, image=img, is_main=(i == 0))
            messages.success(request, 'Múlk sátti qosıldı!')
            return redirect('property_detail', pk=prop.pk)
    else:
        form = PropertyForm()
    return render(request, 'properties/create.html', {'form': form})


@login_required
def property_edit(request, pk):
    prop = get_object_or_404(Property, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=prop)
        if form.is_valid():
            form.save()
            images = request.FILES.getlist('images')
            for i, img in enumerate(images):
                PropertyImage.objects.create(property=prop, image=img)
            messages.success(request, 'Múlk sátti jańalandı!')
            return redirect('property_detail', pk=prop.pk)
    else:
        form = PropertyForm(instance=prop)
    return render(request, 'properties/create.html', {'form': form, 'prop': prop})


@login_required
def property_delete(request, pk):
    prop = get_object_or_404(Property, pk=pk, owner=request.user)
    if request.method == 'POST':
        prop.delete()
        messages.success(request, 'Múlk óshirildi!')
        return redirect('my_listings')
    return render(request, 'properties/confirm_delete.html', {'prop': prop})


@login_required
def toggle_favorite(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, property=prop)
    if not created:
        fav.delete()
        is_fav = False
    else:
        is_fav = True
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_favorite': is_fav})
    return redirect('property_detail', pk=pk)


@login_required
def my_listings(request):
    props = Property.objects.filter(owner=request.user)
    return render(request, 'properties/my_listings.html', {'properties': props})


@login_required
def my_favorites(request):
    favs = Favorite.objects.filter(user=request.user).select_related('property')
    return render(request, 'properties/favorites.html', {'favorites': favs})


@login_required
def profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        profile.phone = request.POST.get('phone', '')
        profile.save()
        messages.success(request, 'Profil jańalandı!')
        return redirect('profile')
    return render(request, 'properties/profile.html', {'profile': profile})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, 'Dizimnen ótiw sátti boldı!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def ai_assistant(request):
    return render(request, 'properties/ai_assistant.html')


def ai_chat(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    data = json.loads(request.body)
    user_message = data.get('message', '')
    history = data.get('history', [])

    if not user_message:
        return JsonResponse({'error': 'No message'}, status=400)

    system_prompt = """Sen Qaraqalpaqstan kóshpes múlk platformasınıń AI járdemshisisıń. 
Paydalanıwshılarǵa úy, páter, jer hám kommerciyalıq múlklerdi tabıwda, satıwda hám ijaraga alıwda járdem beresiń.
Qısqa, anıq hám paylı juwaplar ber. Tilde Qaraqalpaqsha, Ózbeksha yaki Russha sóylesin - qayısında sóylesse, sonday juwap ber."""

    messages_payload = []
    for h in history[-10:]:
        messages_payload.append({'role': h['role'], 'content': h['content']})
    messages_payload.append({'role': 'user', 'content': user_message})

    try:
        resp = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {settings.OPENROUTER_API_KEY}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'https://koshpes-mulk.uz',
                'X-Title': 'Koshpes Mulk',
            },
            json={
                'model': settings.OPENROUTER_MODEL,
                'messages': [{'role': 'system', 'content': system_prompt}] + messages_payload,
                'max_tokens': 500,
                'temperature': 0.7,
            },
            timeout=30
        )
        resp.raise_for_status()
        result = resp.json()
        reply = result['choices'][0]['message']['content']
        return JsonResponse({'reply': reply})
    except Exception as e:
        return JsonResponse({'reply': 'Qáte júz berdi. Qaytaldan urınıń. / Ошибка. Попробуйте снова.'})
