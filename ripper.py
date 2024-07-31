import requests
import shutil
from pprint import pprint
import re
import os
from PIL import Image

# def test(url):
#     response = requests.get(url, stream=True)
#     with open('Comic_ORV/chapter1.webp', 'wb') as out_file:
#         shutil.copyfileobj(response.raw, out_file)


# test("https://gg.asuracomic.net/storage/comics/105/c2c36d3d-ec83-4556-9cfc-9d0fb23b08c7/12.webp")


from PIL import Image
import os


def concatenate_vertical(folder_path, output_path):
    file_paths = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.endswith(".webp")
    ]
    images = [Image.open(fp) for fp in file_paths]
    images.sort(key=lambda x: x.filename)
    total_height = sum(image.height for image in images)
    max_width = max(image.width for image in images)
    new_image = Image.new("RGB", (max_width, total_height))
    current_height = 0
    for image in images:
        if image.width != max_width:
            image = image.resize(
                (max_width, int(image.height * max_width / image.width)),
                Image.ANTIALIAS,
            )

        new_image.paste(image, (0, current_height))
        current_height += image.height
    new_image.save(output_path)
    for file_path in file_paths:
        os.remove(file_path)
        print(f"Removed file: {file_path}")



def saveChapter(comic_folder_name, beg_chapter, end_chapter, comic_url_up_to_chapter):
    comic_folder_name = "Comic_" + comic_folder_name
    curr = os.getcwd()
    full_path = os.path.join(curr, comic_folder_name)
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    for chapter in range(beg_chapter, end_chapter + 1):
        full_path = os.path.join(curr, comic_folder_name, str(chapter))
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        imgSet = set()
        url = comic_url_up_to_chapter + str(chapter)
        response = str(requests.get(url).content)
        pattern = r"https://gg\.asuracomic\.net/storage/comics/[^/]+/[^/]+/[^/]+\.webp"
        matches = re.findall(pattern, response)
        for match in matches:
            imgSet.add(match)
        imgList = list(imgSet)
        imgList.sort()
        for img in imgList:
            response = requests.get(img, stream=True)
            with open(
                full_path + "/" + img[-7:], "wb"
            ) as out_file:
                shutil.copyfileobj(response.raw, out_file)
        print(f"Chapter {chapter} done.")
        # concatenate_vertical(
        #     full_path,
        #     full_path + "/" + str(chapter) + ".webp",
        # )


saveChapter(
    "ORV",
    125,
    150,
    "https://asuracomic.net/series/omniscient-readers-viewpoint-ad808d5b/chapter/",
)
