# main.py
import asyncio
from config import YOUR_COOKIE_STRING
from ozon_client import fetch_ozon_rating

async def main():
    print("=== Парсер рейтинга товаров Ozon ===")
    article = input("Введите артикул товара (например, 1066986718): ").strip()
    
    if not article.isdigit():
        print("Ошибка: Артикул должен состоять только из цифр.")
        return

    # Проверка наличия пользовательских Cookie
    if YOUR_COOKIE_STRING == "ВСТАВЬТЕ_ВАШИ_COOKIES_СЮДА":
        print("[!] Внимание: Вы не добавили Cookie в файл config.py.")
        print("[!] Скрипт может получить ошибку 403 (Forbidden) от системы защиты Cloudflare.")
        print("[!] Пожалуйста, обновите конфигурацию перед запуском скрипта.\n")

    # Очистка строки Cookie от случайных переносов строк (во избежание Header Injection)
    clean_cookie = YOUR_COOKIE_STRING.replace('\n', '').replace('\r', '').strip()
        
    print(f"Отправка запроса для артикула {article}...")
    
    # Асинхронный вызов функции парсинга
    rating = await fetch_ozon_rating(article, clean_cookie)
    
    if rating is not None:
        print(f"[+] Успех! Рейтинг товара {article}: {rating}")
    else:
        print(f"[-] Не удалось получить рейтинг для товара {article}.")

if __name__ == "__main__":
    # Запуск асинхронного event-loop
    asyncio.run(main())