# ozon_client.py
import aiohttp
import re
from config import HEADERS

async def fetch_ozon_rating(article: str, my_cookie: str) -> float | None:
    """
    Асинхронно получает рейтинг товара с маркетплейса Ozon по его артикулу.
    Использует сессию пользователя (Cookie) для обхода WAF (Cloudflare).
    """
    # Выполняем прямой запрос на региональный домен для обхода клиентского JS-редиректа
    url = f"https://uz.ozon.com/product/{article}/"
    
    headers = HEADERS.copy()
    headers["Cookie"] = my_cookie

    # Используем контекстный менеджер для безопасного закрытия сессии
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.get(url, timeout=15) as response:
                if response.status != 200:
                    print(f"[-] Ошибка: сервер вернул HTTP-статус {response.status}")
                    return None
                
                html = await response.text()
                
                # Поиск скрытых данных о рейтинге в JSON/SEO разметке страницы (state/schema)
                # Попытка 1: Валидный JSON (Schema.org / Google SEO)
                match = re.search(r'"ratingValue"[\s]*:[\s]*"?([0-9.]+)"?', html)
                
                # Попытка 2: Внутренний state Ozon API
                if not match:
                    match = re.search(r'"rating"[\s]*:[\s]*([0-9.]+)', html)
                    
                # Попытка 3: HTML-экранированный JSON (асинхронная подгрузка данных)
                if not match:
                    match = re.search(r'&quot;ratingValue&quot;\s*:\s*(?:&quot;|")?([0-9.]+)', html)
                    
                if not match:
                    match = re.search(r'&quot;rating&quot;\s*:\s*([0-9.]+)', html)
                    
                # Попытка 4: Обычный текст на странице
                if not match:
                    match = re.search(r'(?:score|rating|Рейтинг)[\D]{1,15}([0-5]\.[0-9])', html, re.IGNORECASE)
                
                if match:
                    return float(match.group(1))
                else:
                    print("[-] Рейтинг не найден. Возможно, изменилась структура DOM или сработала защита (капча).")
                    return None
                    
        except Exception as e:
            print(f"[-] Произошла непредвиденная сетевая ошибка: {e}")
            return None