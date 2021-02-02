import os

import img2pdf
from PIL import Image

card_wide_poker = 750
card_height_poker = 1050
card_wide_minieuro = 530
card_height_minieuro = 800
origin_x = 144
origin_y = 144
cards = os.listdir(r"cards/")


def execute(cards_per_sheet, cards_per_line, cards_per_column, file_name, card_wide, card_height):
    print("Let's generate the pdf for printing Mini Euro Cards pretty")
    folio = Image.new("RGB", (2480, 3508), "white")

    pagecount = 1
    for i, card in enumerate(cards, start=0):

        pageCoordIndex = i % cards_per_sheet
        x = origin_x + (card_wide * (pageCoordIndex % cards_per_column))
        y = origin_y + (card_height * (pageCoordIndex // cards_per_line))
        folio.paste(Image.open(r"cards/" + card), (x, y))

        if pageCoordIndex == 15 or (card is cards[-1]):
            file_path = f"Page{pagecount}.jpg"
            folio.save(file_path, dpi=(300.0, 300.0))
            folio = Image.new("RGB", (2480, 3508), "white")
            pagecount += 1

    merge_images_into_pdf(file_name)


def merge_images_into_pdf(name):
    with open(name, "wb") as pdfMerged:
        imgs = []
        for r, _, imgToInclude in os.walk("."):
            for file_name in imgToInclude:
                if not file_name.startswith("Page"):
                    continue
                imgs.append(os.path.join(r, file_name))
        pdfMerged.write(img2pdf.convert(imgs))
        for img_to_remove in imgs:
            os.remove(img_to_remove)


choice = input("1-Poker, 2-Minieuro: ")
if choice == "1":
    execute(9, 3, 3, "poker_merged.pdf", card_wide_poker, card_height_poker)
elif choice == "2":
    execute(16, 4, 4, "mini_euro_merged.pdf", card_wide_minieuro, card_height_minieuro)
else:
    exit(-1)
