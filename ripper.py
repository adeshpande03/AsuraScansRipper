import requests
import shutil
from pprint import pprint
import re
from PIL import Image
import sys
import os


def convert_and_concatenate_vertical(folder_path, output_path):
    # List all webp files in the folder
    file_paths = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.endswith(".webp")
    ]
    converted_images = []
    file_paths.sort()
    # Convert webp to png
    for fp in file_paths:
        image = Image.open(fp)
        # Ensure conversion to a format supporting transparency
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        png_path = fp.rsplit(".", 1)[0] + ".png"  # Generate PNG path
        image.save(png_path, format="PNG")
        converted_images.append(Image.open(png_path))
    total_height = sum(img.height for img in converted_images)
    max_width = max(img.width for img in converted_images)
    new_image = Image.new("RGBA", (max_width, total_height))
    current_height = 0
    for img in converted_images:
        if img.width != max_width:
            img = img.resize(
                (max_width, int(img.height * max_width / img.width)), Image.LANCZOS
            )
        new_image.paste(img, (0, current_height), img)
        current_height += img.height
    new_image.save(output_path)
    for fp in file_paths + [img.filename for img in converted_images]:
        os.remove(fp)


def saveChapter(comic_folder_name, beg_chapter, end_chapter, comic_url_up_to_chapter):
    comic_folder_name = "Comic_" + comic_folder_name
    curr = os.getcwd()
    full_path = os.path.join(curr, comic_folder_name)
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    for chapter in range(int(beg_chapter), int(end_chapter) + 1):
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
            with open(full_path + "/" + img[-7:], "wb") as out_file:
                shutil.copyfileobj(response.raw, out_file)
        # convert_and_concatenate_vertical(
        #     f"{full_path}",
        #     f"{full_path}/{chapter}.png",
        # )
        # print(f"Chapter {chapter} done.")


saveChapter(
    "Return of the Mount Hua Sect", #folder title
    sys.argv[1], #beg
    sys.argv[2], #end
    "https://asuracomic.net/series/return-of-the-mount-hua-sect-e35abd30/chapter/", #link up to /chapter/
)
