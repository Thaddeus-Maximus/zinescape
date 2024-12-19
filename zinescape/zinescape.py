from pypdf import PdfWriter, PdfReader
from pypdf.generic import RectangleObject
import argparse

#A4_WIDTH = 595.28  # A4 width in points
#A4_HEIGHT = 841.89  # A4 height in points

LETTER_WIDTH = 612
LETTER_HEIGHT = 792

def template(f_name, n_pages, width, height):

    width *= 96
    height *= 96 # 8.5
    spacing = 96 #1.0
    margin = 48 #0.5

    doc = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <svg
       width="%d"
       height="%d"
       viewBox="0 0 %d %d"
       version="1.1"
       id="svg5"
       inkscape:version="1.2.2 (b0a8486541, 2022-12-01)"
       xml:space="preserve"
       xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
       xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
       xmlns="http://www.w3.org/2000/svg"
       xmlns:svg="http://www.w3.org/2000/svg"><defs
         id="defs21" /><sodipodi:namedview
         id="namedview7"
         pagecolor="#ffffff"
         bordercolor="#666666"
         borderopacity="1.0"
         inkscape:pageshadow="2"
         inkscape:pageopacity="0.0"
         inkscape:pagecheckerboard="0"
         inkscape:document-units="in"
         inkscape:snap-global="false"
         fit-margin-top="0"
         fit-margin-left="0"
         fit-margin-right="0"
         fit-margin-bottom="0"
         units="in"
         width="%din"
         inkscape:showpageshadow="2"
         inkscape:deskcolor="#d1d1d1"
         showguides="false"
         inkscape:lockguides="false"><inkscape:grid
       type="xygrid"
       id="grid1046"
       originx="0"
       originy="0"
       spacingy="1"
       spacingx="1"
       units="in"
       visible="false" />\n""" % (width, height, width, height, width)

    for i in range(n_pages):
        doc += '<inkscape:page'
        if i == n_pages - 1:
            doc += ' x="%f"' % (-width)
        else:
            doc += ' x="%f"' % ((i)*width + ((i/2) + (i%2)/2) * spacing)
        doc += ' y="0"'
        doc += ' width="%f"' % width
        doc += ' height="%f"' % height
        doc += ' id="page_%d"' % i
        doc += ' margin="%f"' % margin
        doc += ' bleed="0"/>\n'

    doc += '</svg>'

    with open(f_name, 'w') as f:
        f.write(doc)

def nup(input_pdf_path, output_pdf_path, rows=1, cols=2):
    is_landscape=True
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    num_pages = len(reader.pages)
    pages_per_sheet = rows*cols

    booklet_indices = []
    for i in range(int(len(reader.pages)/4)):
        booklet_indices.append(i*2)
        booklet_indices.append(len(reader.pages)-i*2-1)
        booklet_indices.append(i*2+1)
        booklet_indices.append(len(reader.pages)-i*2-2)

    if is_landscape:
        width = LETTER_HEIGHT
        height = LETTER_WIDTH
    else:
        width = LETTER_WIDTH
        height = LETTER_HEIGHT

    for i in range(0, num_pages, pages_per_sheet):
        new_page = writer.add_blank_page(width=width, height=height)

        page_width = width / cols
        page_height = height / rows

        positions = [(col * page_width, (rows - 1 - row) * page_height) for row in range(rows) for col in range(cols)]

        for j in range(pages_per_sheet):
            if i + j < num_pages:
                page = reader.pages[booklet_indices[i + j]]

                # Calculate the scale factor to maintain aspect ratio
                scale_x = page_width / page.mediabox.width
                scale_y = page_height / page.mediabox.height
                scale = min(scale_x, scale_y)  # Use the smaller scale to ensure it fits

                page.scale_by(scale)

                if i % 4 >= 2:
                    # Adjust the positions to center the page horizontally and vertically
                    x_offset = (page_width - page.mediabox.width) / 2
                    y_offset = (page_height - page.mediabox.height) / 2

                    # Translate the page to the correct position
                    position = positions[j]
                    translation_matrix = [1, 0, 0, 1, position[0] + x_offset, position[1] + y_offset]
                    page.mediabox = RectangleObject([0, 0, page_width, page_height])
                    new_page.merge_transformed_page(page, translation_matrix)
                else:
                    # Adjust the positions to center the page horizontally and vertically
                    x_offset = (page_width - page.mediabox.width) / 2
                    y_offset = (page_height - page.mediabox.height) / 2

                    # Translate the page to the correct position
                    position = positions[j]
                    translation_matrix = [-1, 0, 0, -1, page_width + position[0] + x_offset, page_height + position[1] + y_offset]
                    page.mediabox = RectangleObject([0, 0, page_width, page_height])
                    new_page.merge_transformed_page(page, translation_matrix)

    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)


def cli():
    parser = argparse.ArgumentParser(
                        prog='zinescape',
                        description='Utilities for making zines',
                        epilog='epilog here')

    parser.add_argument('command')
    parser.add_argument('-W', '--width')
    parser.add_argument('-H', '--height')
    parser.add_argument('-N', '--n_pages')
    parser.add_argument('-R', '--rows', default=1)
    parser.add_argument('-C', '--cols', default=2)
    parser.add_argument('filename')
    parser.add_argument('out_fn', nargs='?')

    args = parser.parse_args()
    print(args)

    if args.command == 'compile':
        out_fn = args.out_fn
        if out_fn == None:
            out_fn = args.filename.split('.')[0] + '.compiled.' + args.filename.split('.')[1]
        nup(args.filename, out_fn, args.rows, args.cols)

    if args.command == 'template':
        if args.width == None:
            args.width=5.5
        if args.height == None:
            args.height=8.5
        template(args.filename, int(args.n_pages), float(args.width), float(args.height))