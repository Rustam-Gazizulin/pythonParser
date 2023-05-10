import requests
from tqdm import tqdm
import json
import os


headers = {'Authorization': f'{os.getenv("API_KEY")}'}
proxies = {'https': f'http://{os.getenv("LOGIN")}:{os.getenv("PASSWORD")}@45.153.20.222:12437'}


def scrap_pexels(query=''):
    query_str = f"https://api.pexels.com/v1/search?query={query}&per_page=20&orientation=landscape"
    response = requests.get(url=query_str, headers=headers, proxies=proxies)

    if response.status_code != 200:
        return f'Ошибка: Статус код - {response.status_code}, {response.json()}'

    img_dir_path = '_'.join(i for i in query.split(' ') if i.isalnum())

    if not os.path.exists(img_dir_path):
        os.makedirs(img_dir_path)

    json_data = response.json()

    with open(f'result_{query}.json', 'w') as file:
        json.dump(json_data, file, indent=4, ensure_ascii=False)

    images_count = json_data.get('total_results')

    if not json_data.get('next_page'):
        img_urls = [item.get('src').get('small') for item in json_data.get('photos')]
        download_images(img_list=img_urls, img_dir_path=img_dir_path)
    else:
        print(f'[INFO] Всего изображений: {images_count}. Сохранение может занять какое-то время.')
        image_list_urls = []

        # В range можно передать количество листов из выдачи которое требуется скачать
        for page in range(1, 3):
            query_str = f'{query_str}&page={page}'
            response = requests.get(url=query_str, headers=headers, proxies=proxies)
            json_data = response.json()
            img_urls = [item.get('src').get('small') for item in json_data.get('photos')]
            image_list_urls.extend(img_urls)
        download_images(img_list=image_list_urls, img_dir_path=img_dir_path)


def download_images(img_list, img_dir_path=''):

    #  функция tqdm интерактивный статус бар скачивания изображений
    for item_url in tqdm(img_list):
        response = requests.get(url=item_url, proxies=proxies)
        item_url = item_url.split("-")[-1]
        if response.status_code == 200:
            with open(f'./{img_dir_path}/{item_url.split("?")[-2]}', 'wb') as file:
                file.write(response.content)

        else:
            print("Что то пошло не так при скачивании")


def main():
    query = input("Введите ключевую фразу для поиска картинок: ")
    scrap_pexels(query=query)


if __name__ == '__main__':
    main()

