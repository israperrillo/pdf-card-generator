import argparse
import os

import img2pdf
from PIL import Image

card_wide_poker = 750
card_height_poker = 1050
card_wide_minieuro = 530
card_height_minieuro = 800
origin_x = 144
origin_y = 144


class Cards2Pdf:
    cards_folder = os.listdir(r"cards/")

    def __init__(self, card_folder=r"cards/"):
        self.cards_folder = card_folder

    def execute(self, cards_per_sheet, cards_per_line, cards_per_column, file_name, card_wide, card_height):
        print("Let's generate the pdf for printing Mini Euro Cards pretty")
        folio = Image.new("RGB", (2480, 3508), "white")

        pagecount = 1
        for i, card in enumerate(self.cards_folder, start=0):

            page_coord_index = i % cards_per_sheet
            x = origin_x + (card_wide * (page_coord_index % cards_per_column))
            y = origin_y + (card_height * (page_coord_index // cards_per_line))
            folio.paste(Image.open(r"cards/" + card), (x, y))

            if page_coord_index == (cards_per_sheet-1) or (card is self.cards_folder[-1]):
                file_path = f"Page{pagecount}.jpg"
                folio.save(file_path, dpi=(300.0, 300.0))
                folio = Image.new("RGB", (2480, 3508), "white")
                pagecount += 1

        self.merge_images_into_pdf(file_name)

    @staticmethod
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


def default_settings(card_type):
    if card_type == 'minieuro':
        card_per_sheet = 16
        card_per_column = 4
        card_per_row = 4
        file_input = "mini_euro_merged.pdf"
        card_wide = card_wide_minieuro
        card_height = card_height_minieuro
    elif card_type == 'poker':
        card_per_sheet = 9
        card_per_column = 3
        card_per_row = 3
        file_input = "poker_merged.pdf"
        card_wide = card_wide_poker
        card_height = card_height_poker

    return card_per_sheet, card_per_column, card_per_row, file_input, card_wide, card_height


def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--minieuro", help="for minieuro cards", action="store_true")
    parser.add_argument("--poker", help="for poker cards", action="store_true")
    parser.add_argument("-s", "--card_per_sheet", type=int, help="cards per sheet")
    parser.add_argument("-l", "--card_per_line", type=int, help="cards per line")
    parser.add_argument("-c", "--card_per_column", type=int, help="cards_per_column")
    parser.add_argument("-f", "--file_name", help="output filename")
    parser.add_argument("-i", "--input_folder", help="input folder", default=r"cards/")

    return parser.parse_args()


if __name__ == '__main__':

    args = read_args()

    if not args.minieuro or not args.poker:
        args.print_help()
        exit(1)

    card_type = ''
    if args.minieuro:
        card_type = 'minieuro'
    elif args.poker:
        card_type = 'poker'

    card2pdf = Cards2Pdf(args.input_folder)

    card_per_sheet, card_per_column, card_per_row, file_input, card_wide, card_height = default_settings(card_type)

    if args.card_per_sheet:
        card_per_sheet = args.card_per_sheet
    if args.card_per_column:
        card_per_column = args.card_per_column
    if args.card_per_row:
        card_per_row = args.card_per_row
    if args.file_input:
        file_input = args.file_input

    card2pdf.execute(cards_per_sheet=card_per_sheet, cards_per_column=card_per_column, cards_per_line=card_per_row,
                     file_name=file_input, card_wide=card_wide, card_height=card_height)
