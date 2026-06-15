import asyncio
import aiohttp
import re

async def fetch_ozon_rating(article: str, my_cookie: str) -> float | None:
    # MANA SHU YER O'ZGARDI: www.ozon.ru o'rniga uz.ozon.com ishlatamiz
    url = f"https://uz.ozon.com/product/{article}/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Connection": "keep-alive",
        "Cookie": my_cookie
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.get(url, timeout=15) as response:
                if response.status != 200:
                    print(f"[-] Ошибка: сервер вернул статус {response.status}")
                    return None
                
                html = await response.text()
                
                match = re.search(r'"ratingValue"[\s]*:[\s]*"?([0-9.]+)"?', html)
                
                if not match:
                    match = re.search(r'"rating"[\s]*:[\s]*([0-9.]+)', html)
                    
                if not match:
                    match = re.search(r'&quot;ratingValue&quot;\s*:\s*(?:&quot;|")?([0-9.]+)', html)
                    
                if not match:
                    match = re.search(r'&quot;rating&quot;\s*:\s*([0-9.]+)', html)
                    
                if not match:
                    match = re.search(r'(?:score|rating|Рейтинг)[\D]{1,15}([0-5]\.[0-9])', html, re.IGNORECASE)
                
                if match:
                    return float(match.group(1))
                else:
                    print("[-] Рейтинг не найден в HTML. Ozon ma'lumotlarni JavaScript orqali asinxron yuklayotgan bo'lishi mumkin.")
                    return None
                    
        except Exception as e:
            print(f"[-] Произошла ошибка сети: {e}")
            return None

async def main():
    print("=== Ozon Rating Checker ===")
    article = input("Введите артикул товара (например, 1066986718): ").strip()
    
    if not article.isdigit():
        print("Артикул должен состоять только из цифр.")
        return

    YOUR_COOKIE_STRING = "__Secure-ETC=047a14347c9f72c768568804c5116ee6; __Secure-access-token=12.0.SFTh--jTTZ-7axczZmdRgg.29.AYmWh1YKNUzVk0ZXsdVZlqlnSqRKrdJzT1RKUJ-1J5f2DGeu6riFnH364FiCJouV31Q_cQgY8oMqR-_R2Ca4kPr9uXMbbFq8NnnyOW1PONag3GV2izTOIDZ50mgON26tag..20260615112603.0.ohDvoXJZVfmGNT8hP0l-AS65e9kuH4q7rDLtUwmBQN0.150dbf05b44b52d18; __Secure-refresh-token=12.0.SFTh--jTTZ-7axczZmdRgg.29.AYmWh1YKNUzVk0ZXsdVZlqlnSqRKrdJzT1RKUJ-1J5f2DGeu6riFnH364FiCJouV31Q_cQgY8oMqR-_R2Ca4kPr9uXMbbFq8NnnyOW1PONag3GV2izTOIDZ50mgON26tag..20260615112603.0.pxLYbcBVBZ8bEawSsp5wS-ZFjL5zVJoiOOWEAacOTTU.1cdcd7de6d6ea79b8; __Secure-ab-group=29; __Secure-user-id=0; xcid=3bce7406845c4b4dd6c4598c1436232f; __Secure-ext_xcid=3bce7406845c4b4dd6c4598c1436232f; rfuid=LTE5NTAyNjU0NzAsMTI0LjA0MzQ3NTI3NTE2MDc0LDE4MTczODQwMTEsLTEsLTE4NjkxNzMyMSxXM3NpYm1GdFpTSTZJbEJFUmlCV2FXVjNaWElpTENKa1pYTmpjbWx3ZEdsdmJpSTZJbEJ2Y25SaFlteGxJRVJ2WTNWdFpXNTBJRVp2Y20xaGRDSXNJbTFwYldWVWVYQmxjeUk2VzNzaWRIbHdaU0k2SW1Gd2NHeHBZMkYwYVc5dUwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjBzZXlKMGVYQmxJam9pZEdWNGRDOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5WFgwc2V5SnVZVzFsSWpvaVEyaHliMjFsSUZCRVJpQldhV1YzWlhJaUxDSmtaWE5qY21sd2RHbHZiaUk2SWxCdmNuUmhZbXhsSUVSdlkzVnRaVzUwSUVadmNtMWhkQ0lzSW0xcGJXVlVlWEJsY3lJNlczc2lkSGx3WlNJNkltRndjR3hwWTJGMGFXOXVMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4wc2V5SjBlWEJsSWpvaWRHVjRkQzl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOVhYMHNleUp1WVcxbElqb2lRMmh5YjIxcGRXMGdVRVJHSUZacFpYZGxjaUlzSW1SbGMyTnlhWEIwYVc5dUlqb2lVRzl5ZEdGaWJHVWdSRzlqZFcxbGJuUWdSbTl5YldGMElpd2liV2x0WlZSNWNHVnpJanBiZXlKMGVYQmxJam9pWVhCd2JHbGpZWFJwYjI0dmNHUm1JaXdpYzNWbVptbDRaWE1pT2lKd1pHWWlmU3g3SW5SNWNHVWlPaUowWlhoMEwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjFkZlN4N0ltNWhiV1VpT2lKTmFXTnliM052Wm5RZ1JXUm5aU0JRUkVZZ1ZtbGxkMlZ5SWl3aVpHVnpZM0pwY0hScGIyNGlPaUpRYjNKMFlXSnNaU0JFYjJOMWJXVnVkQ0JHYjNKdFlYUWlMQ0p0YVcxbFZIbHdaWE1pT2x0N0luUjVjVpT2lKaGNIQnNhV05oZEdsdmJpOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5TEhzaWRIbHdaU0k2SW5SbGVIUXZjR1JtSWl3aWMzVm1abWw0WlhNaU9pSndaR1lpZlYxOUxIc2libUZ0WlNJNklsZGxZa3RwZENCaWRXbHNkQzFwYmlCUVJFWWlMQ0prWlhOamNtbHdkR2x2YmlJNklsQnZjblJoWW14bElFUnZZM1Z0Wlc1MElFWnZjbTFoZENJc0ltMXBiV1ZVZVhCbGN5STZXM3NpZEhsd1pTSTZJbUZ3Y0d4cFkyRjBhVzl1TDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMHNleUowZVhCbElqb2lkR1Y0ZEM5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDFkLFd5SmxiaTFWVXlKZCwwLDEsMCwyNCwyMzc0MTU5MzAsMzIsMjI3MTI2NTIwLDAsMSwwLC00OTEyNzU1MjMsUjI5dloyeGxJRWx1WXk0Z1RtVjBjMk5oY0dVZ1IyVmphMjhnVEdsdWRYZ2dlRGcyWHpZMElEVXVNQ0FvV0RFeE95Qk1hVzUxZUNCNE9EWmZOalFwSUVGd2NHeGxWMlZpUzJsMEx6VXpOeTR6TmlBb1MwaFVUVXdzSUd4cGEyVWdSMlZqYTI4cElFTm9jbTl0WlM4eE5Ea3VNQzR3TGpBZ1UyRm1ZWEpwTHpVek55NHpOaUF5TURBek1ERXdOeUJOYjNwcGJHeGgsZXlKamFISnZiV1VpT25zaVlYQndJanA3SW1selNXNXpkR0ZzYkdWa0lqcG1ZV3h6WlN3aVNXNXpkR0ZzYkZOMFlYUmxJanA3SWtSSlUwRkNURVZFSWpvaVpHbHpZV0pzWldRaUxDSkpUbE5VUVV4TVJVUWlPaUpwYm5OMFlXeHNaV1FpTENKT1QxUmZTVTVUVkVGTVRFVkVJam9pYm05MFgybHVjM1JoYkd4bFpDSjlMQ0pTZFc1dWFXNW5VM1JoZEdVaU9uc2lRMEZPVGs5VVgxSlZUaUk2SW1OaGJtNXZkRjl5ZFc0aUxDSlNSVUZFV1Y5VVQxOVNWVTRpT2lKeVpXRmtlVjkwYjE5eWRXNGlMQ0pTVlU1T1NVNUhJam9pY25WdWJtbHVaeUo5ZlgxOSw2NSwxNzUyNzg1NjcxLDEsMSwtMSwxNjk5OTU0ODg3LDE2OTk5NTQ4ODcsMTE2NDI0Njk1OSwxNg==; abt_data=7.Qq3oD1jRrDE825qdiF2u37USdffMufQ7iJXSrE7DGGbXHtaB9AbKl_mwRDxnpArJdlNenFk_Ighm9iemoXEQH5mE_2BAr3DhgVyPlzrTG3g9OAH7FujOxN6iT4k__CKanKE-pae8uakF_Z79SR04LBauZYptk57m6jn0QwkKOHsbAotnY8-J6R-7kR4ysQcQ-xa5PzAwsy5n2F3Yf_VDE5fiP-WfqCtiMEQzzorpZ9jqU7hV7XCSBy8c-TstpTUfHBBLIMsHcOu1gJS6kMRi1zfcGfV46ACpBwPHdCmYOZsYthW1rBAafGb_qiOfoMl9oHoPG5Krt3DWy6PIBp6wyQCFC8Eqd9S_1gcjJXyHn2-Xgnl9kNohiyJbKJXZcvGMaWMbmCfvjQLlWcVgZ9NcsDpwOQNvXYgzkbf5TXKk-1GMg_qXMmhE1pa9FaVFCyzpHUAxpS0kP9t70ku7UdKpvbQ9KtNUmdm__6StMQn9uoud3uNzWDi7WgA7BjXjCJTpNeQqu8NBt-nH-soXhReH8j4ZvxYGU2VOcuS0JlRArnr-mwQ"
    
    clean_cookie = YOUR_COOKIE_STRING.replace('\n', '').replace('\r', '').strip()
        
    print(f"Отправка запроса для артикула {article}...")
    rating = await fetch_ozon_rating(article, clean_cookie)
    
    if rating is not None:
        print(f"[+] Успех! Рейтинг товара {article}: {rating}")

if __name__ == "__main__":
    asyncio.run(main())