# myapp/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_date
from datetime import date

UZB_REGIONS = {
    "andijon", "buxoro", "farg'ona", "jizzax", "xorazm", "namangan",
    "navoiy", "sirdaryo", "qashqadaryo", "samarqand", "surxondaryo",
    "toshkent", "toshkent viloyati", "respublika karakalpakstan", "nukus"
}

def _normalize_region(name: str) -> str:
    if not isinstance(name, str):
        return ""
    return name.strip().lower()

@require_http_methods(["GET", "POST"])
def check_age(request):
    if request.method == "GET":
        return render(request, "myapp/check_age.html")  # отдаём HTML форму

    # POST: обрабатываем данные и возвращаем JSON
    age = request.POST.get('age')
    birthdate = request.POST.get('birthdate')

    if age:
        try:
            age = int(age)
        except (ValueError, TypeError):
            return JsonResponse({"ok": False, "message": "Неверное значение age. Ожидается целое число."}, status=400)
    elif birthdate:
        bd = parse_date(birthdate)
        if bd is None:
            return JsonResponse({"ok": False, "message": "Неверный формат birthdate. Ожидается YYYY-MM-DD."}, status=400)
        today = date.today()
        age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
    else:
        return JsonResponse({"ok": False, "message": "Укажите 'age' или 'birthdate'."}, status=400)

    is_adult = age >= 18
    return JsonResponse({"ok": True, "is_adult": is_adult, "age": age})

@require_http_methods(["GET", "POST"])
def regions(request):
    if request.method == "GET":
        return render(request, "myapp/regions.html")  # отдаём HTML форму

    region = request.POST.get('region', '')
    if not region:
        return JsonResponse({"ok": False, "message": "Укажите поле 'region'."}, status=400)

    norm = _normalize_region(region)
    exists = norm in UZB_REGIONS
    return JsonResponse({"ok": True, "exists": exists, "normalized": norm})

