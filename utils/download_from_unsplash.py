import requests
import os

def download_images_from_api(search_query, download_path, per_page=10, total_images=90):
    access_key = ''
    total_downloaded = 0
    page = 1

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    while total_downloaded < total_images:
        url = (
            f"https://api.unsplash.com/search/photos/"
            f"?query={search_query}&orientation=landscape&client_id={access_key}"
            f"&page={page}&per_page={per_page}"
        )

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break

        data = response.json()
        results = data.get('results', [])
        if not results:
            print("No more images found.")
            break

        for photo in results:
            if total_downloaded >= total_images:
                break
            img_url = photo['urls']['regular']
            category_name = search_query.split()[0].lower()
            img_name = f"{category_name}_{total_downloaded + 1}.jpg"
            img_path = os.path.join(download_path, img_name)

            try:
                img_data = requests.get(img_url).content
                with open(img_path, 'wb') as img_file:
                    img_file.write(img_data)
                print(f"Downloaded: {img_name}")
                total_downloaded += 1
            except Exception as e:
                print(f"Failed to download image: {e}")
                continue

        page += 1

if __name__ == "__main__":
    search_query = "macbook on table"
    download_path = os.path.join("data", search_query.split()[0].lower())
    download_images_from_api(search_query, download_path, total_images=90)
