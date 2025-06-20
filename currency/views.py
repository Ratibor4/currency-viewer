from datetime import datetime, timedelta, date
import requests
from django.shortcuts import render

SUPPORTED_CURRENCIES = [
    "USD", "EUR", "GBP", "JPY", "CHF", "AUD", "CAD", "SEK", "NOK", "DKK", "PLN", "CZK", "HUF", "CNY"
]

def get_exchange_rate(base, target, selected_date):
    url = f"https://api.frankfurter.app/{selected_date}"
    params = {
        "from": base,
        "to": target
    }
    response = requests.get(url, params=params)
    data = response.json()
    print("🔍 Ответ от API:", data)

    if "rates" in data and target in data["rates"]:
        return data["rates"][target]
    return None

def get_exchange_history(base, target, start_date, end_date):
    url = f"https://api.frankfurter.app/{start_date.strftime('%Y-%m-%d')}..{end_date.strftime('%Y-%m-%d')}"
    params = {
        "from": base,
        "to": target
    }
    response = requests.get(url, params=params)
    data = response.json()
    print("📈 История курса:", data)

    rates = data.get("rates", {})
    labels = sorted(rates.keys())
    values = [rates[day][target] for day in labels if target in rates[day]]

    return labels, values

def index(request):
    base = request.GET.get("base", "USD")
    target = request.GET.get("target", "EUR")
    date_str = request.GET.get("date", date.today().isoformat())
    period = request.GET.get("period", "30")

    # Обработка даты
    try:
        end_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        end_date = date.today()

    # Обработка периода
    try:
        days = int(period)
    except ValueError:
        days = 30

    start_date = end_date - timedelta(days=days)

    # Получаем курс
    rate = get_exchange_rate(base, target, end_date.strftime("%Y-%m-%d"))

    # Получаем историю
    labels, values = get_exchange_history(base, target, start_date, end_date)

    context = {
        "base": base,
        "target": target,
        "date": end_date.isoformat(),
        "period": str(period),
        "rate": rate,
        "labels": labels,
        "values": values,
        "currencies": SUPPORTED_CURRENCIES,
    }
    return render(request, "currency/index.html", context)
