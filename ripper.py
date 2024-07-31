import requests
import shutil
from pprint import pprint
import re
import os
from PIL import Image
import sys

# def test(url):
#     response = requests.get(url, stream=True)
#     with open('Comic_ORV/chapter1.webp', 'wb') as out_file:
#         shutil.copyfileobj(response.raw, out_file)


# test("https://gg.asuracomic.net/storage/comics/105/c2c36d3d-ec83-4556-9cfc-9d0fb23b08c7/12.webp")


from PIL import Image
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

    # Calculate total height and maximum width
    total_height = sum(img.height for img in converted_images)
    max_width = max(img.width for img in converted_images)

    # Create a new image with the total height and maximum width
    new_image = Image.new("RGBA", (max_width, total_height))
    # Paste images one below the other
    current_height = 0
    for img in converted_images:
        # If the image width is not the maximum, resize it proportionally
        if img.width != max_width:
            img = img.resize(
                (max_width, int(img.height * max_width / img.width)), Image.LANCZOS
            )
        new_image.paste(
            img,
            (0, current_height),
            img
        )

        current_height += img.height

    # Save the concatenated image
    new_image.save(output_path)

    # Remove the original and converted PNG files
    for fp in file_paths + [img.filename for img in converted_images]:
        os.remove(fp)
        # print(f"Removed file: {fp}")


# chapter = 75
# convert_and_concatenate_vertical(
#     f"/Users/akhildeshpande/Documents/VSCode/Python/AsuraScansRipper/Comic_ORV/{chapter}",
#     f"/Users/akhildeshpande/Documents/VSCode/Python/AsuraScansRipper/Comic_ORV/{chapter}/{chapter}.png",
# )


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
        convert_and_concatenate_vertical(
            f"/Users/akhildeshpande/Documents/VSCode/Python/AsuraScansRipper/Comic_ORV/{chapter}",
            f"/Users/akhildeshpande/Documents/VSCode/Python/AsuraScansRipper/Comic_ORV/{chapter}/{chapter}.png",
        )
        print(f"Chapter {chapter} done.")
        # concatenate_vertical(
        #     full_path,
        #     full_path + "/" + str(chapter) + ".webp",
        # )


saveChapter(
    "ORV",
    sys.argv[1],
    sys.argv[2],
    "https://asuracomic.net/series/omniscient-readers-viewpoint-ad808d5b/chapter/",
)
