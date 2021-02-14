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
    cards_to_process = os.listdir(r"cards/")

    def __init__(self, card_folder=r"cards/"):
        self.cards_to_process = os.listdir(card_folder)

    def execute(self, cards_per_sheet, cards_per_line, cards_per_column, file_name, card_wide, card_height):
        print("Let's generate the pdf for printing cards")
        folio = Image.new("RGB", (2480, 3508), "white")
        pagecount = 1
        for i, card in enumerate(self.cards_to_process, start=0):
            page_coord_index = i % cards_per_sheet
            x = origin_x + (card_wide * (page_coord_index % cards_per_column))
            y = origin_y + (card_height * (page_coord_index // cards_per_line))
            folio.paste(Image.open(r"cards/" + card), (x, y))

            if page_coord_index == (cards_per_sheet - 1) or (card is self.cards_to_process[-1]):
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
    parser = argparse.ArgumentParser(description='Generates a PDF file in dinA4 format with cards set ready to print.')
    parser.add_argument("--minieuro",
                        help="Creates a PDF with 4x4 Mini-euro cards pages under mini_euro_merged.pdf file",
                        action="store_true")
    parser.add_argument("--poker", help="Creates a PDF with 3x3 Poker cards pages under poker_merged.pdf file",
                        action="store_true")
    parser.add_argument("-s", "--card_per_sheet", type=int,
                        help="Number of cards per page (normally cards per row * cards per column")
    parser.add_argument("-r", "--card_per_row", type=int, help="Number of cards per row")
    parser.add_argument("-c", "--card_per_column", type=int, help="Number of cards per column")
    parser.add_argument("-f", "--file_name", help="Name of the created PDF file with extension")
    parser.add_argument("-i", "--input_folder",
                        help="Where the cards are. Must have this format : r\"path-to-folder/\"",
                        default=r"cards/")

    return parser.parse_args()


def print_help_if_not_enough_parameters(args):
    if args.minieuro or args.poker and (
            not args.card_per_sheet or not args.card_per_column or not args.card_per_row):
        return False
    elif not args.card_per_sheet or not args.card_per_column or not args.card_per_row or not args.file_name:
        return True


if __name__ == '__main__':

    args = read_args()

    if print_help_if_not_enough_parameters(args):
        argparse.ArgumentParser().print_usage()
        exit(1)

    card_type = ''
    if args.minieuro:
        card_type = 'minieuro'
    elif args.poker:
        card_type = 'poker'

    card2pdf = Cards2Pdf(args.input_folder)

    card_per_sheet, card_per_column, card_per_row, file_name, card_wide, card_height = default_settings(card_type)

    if args.card_per_sheet:
        card_per_sheet = args.card_per_sheet
    if args.card_per_column:
        card_per_column = args.card_per_column
    if args.card_per_row:
        card_per_row = args.card_per_row
    if args.file_name:
        file_name = args.file_name

    card2pdf.execute(cards_per_sheet=card_per_sheet, cards_per_column=card_per_column, cards_per_line=card_per_row,
                     file_name=file_name, card_wide=card_wide, card_height=card_height)
