from bs4 import BeautifulSoup
import requests
import os
from gtts import gTTS


def parsing_site(address: str, headers: dict) -> tuple:
    """Функція для парсингу тексту з багатьох сторінок"""
    req = requests.get(url=address, headers=headers)
    src = req.text

    soup = BeautifulSoup(src, "lxml")

    pages = soup.find(class_="reading__content js-quote-area").find("p").text
    pages = int(pages[-1])

    print("-" * 20)
    print("[+] read and save 1 page")
    name_book = soup.find(class_="reading__content js-quote-area").find(class_="reading__head clearfix").find("h1").text
    all_book_first_pages = soup.find(class_="reading__content js-quote-area").find(class_="reading__text").text

    if not os.path.exists(f"{name_book}"):
        os.mkdir(f"{name_book}")
    if not os.path.exists(f"{name_book}/text"):
        os.mkdir(f"{name_book}/text")

    all_book_first_pages = all_book_first_pages.replace("\n", "")
    with open(f"{name_book}/text/{name_book}.txt", "w") as file:
        file.write(all_book_first_pages)
    print("[+] Ok 1 page is ready")
    print()

    """Парсимо інші сторінки"""
    for page in range(2, pages + 1):
        print(f"[+] read and save {page} page")
        page = str(page)
        new_url = address[:len(address) - 1] + page
        req = requests.get(url=new_url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")
        all_book_page = soup.find(class_="reading__content js-quote-area").find(class_="reading__text").text
        all_book_page = all_book_page.replace("\n", "")
        with open(f"{name_book}/text/{name_book}.txt", "a") as file:
            file.write(all_book_page)
        print(f"[+] Ok {page} page is ready")
        print()

    with open(f"{name_book}/text/{name_book}.txt") as file:
        book_text = file.read()
    return book_text, name_book


def convert(book_tuple: tuple) -> str:
    """Функція для конвертації тексту в мр3"""
    book_name = book_tuple[1]
    book_text = book_tuple[0]
    audio = gTTS(text=book_text, lang="en")
    print(f"[+] Ok, the last step remains\n[+] Convert {book_name} to mp3 file")

    if not os.path.exists(f"{book_name}/media"):
        os.mkdir(f"{book_name}/media")
    audio.save(f"{book_name}/media/{book_name}.mp3")
    return f"[+] {book_name}.mp3 saved successfully!"


def main():
    """Основна функція"""
    url = "https://readli.net/chitat-online/?b=177645&pg=1"
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"

    }

    print("[+] Processing, pls wait!")

    text_tuple = parsing_site(url, headers)
    print(convert(text_tuple))


if __name__ == "__main__":
    main()
