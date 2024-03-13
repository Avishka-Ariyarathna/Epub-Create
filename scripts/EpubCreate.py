import sys
import os
from ebooklib import epub
import re
import logging
from datetime import datetime

if len(sys.argv) < 2:
    sys.exit("Usage: python script.py <SrcFolder> <DestFolder>")

# Get the value from the command-line arguments
SrcFolder = sys.argv[1]

# Check if the second argument is provided, otherwise use a default value
if len(sys.argv) > 2:
    output_folder_path = sys.argv[2]
    DestFolder = output_folder_path.replace("\\", "/")
else:
    DestFolder = "output"

log_folder = "logs"

folder_path = SrcFolder.replace("\\", "/")

if not os.path.exists(f'{folder_path}/jpg'):os.makedirs(f'{folder_path}/jpg')

img_folder_path = f'{folder_path}/jpg'

last_part = os.path.basename(folder_path)

if not os.path.exists(DestFolder):
    os.makedirs(DestFolder)

if not os.path.exists(log_folder):
    os.makedirs(log_folder)

current_date_time = datetime.now()
formatted_date_time = current_date_time.strftime("%Y-%m-%d %H_%M_%S")
log_file_name = f'{last_part}-{formatted_date_time}.log'
# Configure logging for both console and file output (logs folder)
logging.basicConfig(
    # Log all levels (debug, info, warning, error, critical)
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    # Use a specific file in the logs directory
    filename=os.path.join(log_folder, log_file_name),
    filemode="w"
)

# --------------------------------------------------------------------------------------------------------

try:
    # List all files in the source folder
    all_files = os.listdir(str(folder_path))

    # Filter files by extension
    all_txt_files = [file for file in all_files if file.endswith(".txt")]

    chapter_head = []

    for i in range(99):
        idx = f"{i:02d}"  # Use f-string to format the index with leading zeros
        reserved_chap_files = [file for file in all_files if f"chap{idx}" in file and file.endswith(".txt")]

        # Check if there are any files matching the pattern
        if reserved_chap_files:
            # Print only the first reserved file for each chapter
            chapter_head.append(reserved_chap_files[0])

except FileNotFoundError:
    print(f"Folder not found: {folder_path}")
except Exception as e:
    logging.error(f"File '{folder_path}' not found.")
    print(f"all_files: {e}")

# -----------------------------------------------------------------------------------------------------------

file_path = os.path.join(folder_path, all_txt_files[0])

with open(file_path, 'r', encoding='utf-8') as file:
    input_text = file.readlines()
    sinhala_book_name = input_text[0].strip()
    sinhala_author_name = input_text[2].strip()

# -----------------------------------------------------------------------------------------------------------
first_file_txt_name = all_txt_files[0]

pattern = r'([^-\s]+)-'

# Use re.search to find the match in the filename
match = re.search(pattern, first_file_txt_name)

first_txt = match.group(1)

# Extract book title and author from the first text file
start_index = first_txt.find("(")
end_index = first_txt.find(")")
book_title = first_txt[:start_index].strip()
author_withoutspace = first_txt[start_index + 1:end_index]
author_re = re.findall('[A-Z][a-z]*', author_withoutspace)
author = ' '.join(author_re)

# -----------------------------------------------------------------------------------------------------------
allimg_files = os.listdir(str(img_folder_path))
all_files = os.listdir(folder_path)

all_img_files = [file for file in allimg_files]
processed_content = ''
chapters = []

# This block of code processes a text file containing paragraphs and associated image files.
# The text file is expected to have information about the placement of images (top, middle, or bottom),
# and the code generates HTML content with embedded images for each paragraph.
if all_txt_files:
    for txt_file in all_txt_files:
        pattern = r'\-(\d{3}[a-zA-Z])\-'
        match = re.search(pattern, txt_file)
        captured_word = match.group(1)

        found_files = [file for file in all_img_files if captured_word in file]

        file_path = os.path.join(folder_path, txt_file)

        with open(file_path, 'r', encoding='utf-8') as file:
            input_text = file.read()
            paragraphs = input_text.split('\n\n')

            first_line_skipped = False

        # If there are three image files (top, middle, and bottom), it creates a formatted HTML page with the images in the specified order.
        # The width of each image is determined by a captured percentage from the image file name.
        if len(found_files) == 3:
            processed_content = ''
            txt_page = []

            parts = found_files[0].split("-")
            part1 = found_files[1].split("-")
            part2 = found_files[2].split("-")

            captured_number_with_extension = parts[2]
            captured_number_with_extension1 = part1[2]
            captured_number_with_extension2 = part2[2]

            captured_number = captured_number_with_extension.split(".")[0]
            captured_number1 = captured_number_with_extension1.split(".")[0]
            captured_number2 = captured_number_with_extension2.split(".")[0]

            for i in paragraphs:

                if not first_line_skipped:
                    first_line_skipped = True
                    processed_content += f"<h6>{i.strip()}</h6>\n"
                    processed_content += f'<div style="text-align: center;"> <img style="width: {captured_number2}%;" src="./img/{found_files[2]}"/> </div>'
                    continue
                i.strip()

                if i.endswith(".") or re.match(r'^\d', i) or "." in i or "," in i:
                    processed_content += f"<br/><p>{i.strip()}</p><br/>"

                else:
                    lines = i.splitlines()
                    for l in lines:
                        processed_content += f"<p>{l.strip()}</p>\n"

                # print(f'<img style="width: {captured_number1}%;" src="./img/{found_files[1]}"')

            processed_content += f'<div style="text-align: center;"> <img style="width: {captured_number}%;" src="./img/{found_files[0]}"/> </div>'

            txt_page.append(processed_content)
            full_content = ''.join(txt_page)

            # Calculate the middle index of the full content
            middle_index = len(full_content) // 2

            # Split the content into two parts
            img_page_file_part_I = full_content[:middle_index]
            img_page_file_part_II = full_content[middle_index:]
            mid = f'<div style="text-align: center;"> <img style="width: {captured_number1}%;" src="./img/{found_files[1]}"/> </div>'
            processed_content = f'{img_page_file_part_I}{mid}{img_page_file_part_II}'
            chapters.append(processed_content)

        # If there are two image files, various combinations of image placements (top-bottom, bottom-top, bottom-middle, middle-top) are handled,
        # and corresponding HTML pages are generated accordingly.
        elif len(found_files) == 2:
            processed_content = ''
            parts = found_files[0].split("-")
            part1 = found_files[1].split("-")

            captured_position = parts[1]
            captured_position1 = part1[1]

            captured_number_with_extension = parts[2]
            captured_number_with_extension1 = part1[2]

            captured_number = captured_number_with_extension.split(".")[0]
            captured_number1 = captured_number_with_extension1.split(".")[0]

            if captured_position == 'bottom' and captured_position1 == 'top':

                for i in paragraphs:

                    if not first_line_skipped:
                        first_line_skipped = True
                        processed_content += f"<h6>{i.strip()}</h6>\n"
                        processed_content += f'<div style="text-align: center;"> <img style="width: {captured_number1}%;" src="./img/{found_files[1]}"/> </div>'
                        continue
                    i.strip()

                    if i.endswith(".") or re.match(r'^\d', i) or "." in i or "," in i:
                        processed_content += f"<br/><p>{i.strip()}</p><br/>"

                    else:
                        lines = i.splitlines()
                        for l in lines:
                            processed_content += f"<p>{l.strip()}</p>\n"

                processed_content += f'<div style="text-align: center;"> <img style="width: {captured_number}%;" src="./img/{found_files[0]}"  /> </div>'

            elif captured_position == 'bottom' and captured_position1 == 'middle':

                bm_file = []

                for i in paragraphs:

                    if not first_line_skipped:
                        first_line_skipped = True
                        processed_content += f"<h6>{i.strip()}</h6>\n"
                        continue
                    i.strip()

                    if i.endswith(".") or re.match(r'^\d', i) or "." in i or "," in i:
                        processed_content += f"<br/><p>{i.strip()}</p><br/>"

                    else:
                        lines = i.splitlines()
                        for l in lines:
                            processed_content += f"<p>{l.strip()}</p>\n"

                bm_file.append(processed_content)
                full_content = ''.join(bm_file)

                # Calculate the middle index of the full content
                middle_index = len(full_content) // 2

                # Split the content into two parts
                img_page_file_part_I = full_content[:middle_index]
                img_page_file_part_II = full_content[middle_index:]
                mid = f'<div style="text-align: center;"> <img style="width: {captured_number1}%;" src="./img/{found_files[1]}"/> </div>'
                processed_content = f'{img_page_file_part_I}{mid}{img_page_file_part_II}'

                processed_content += f'<div style="text-align: center;"> <img style="width: {captured_number}%;" src="./img/{found_files[0]}" /> </div>'

            if captured_position == 'middle' and captured_position1 == 'top':

                bt_file = []

                for i in paragraphs:

                    if not first_line_skipped:
                        first_line_skipped = True
                        processed_content += f"<h6>{i.strip()}</h6>\n"
                        processed_content += f'<div style="text-align: center;"> <img style="width: {captured_number1}%;" src="./img/{found_files[1]}"/> </div>'
                        continue
                    i.strip()

                    if i.endswith(".") or re.match(r'^\d', i) or "." in i or "," in i:
                        processed_content += f"<br/><p>{i.strip()}</p><br/>"

                    else:
                        lines = i.splitlines()
                        for l in lines:
                            processed_content += f"<p>{l.strip()}</p>\n"

                bt_file.append(processed_content)
                full_content = ''.join(bt_file)

                # Calculate the middle index of the full content
                middle_index = len(full_content) // 2

                # Split the content into two parts
                img_page_file_part_I = full_content[:middle_index]
                img_page_file_part_II = full_content[middle_index:]
                mid = f'<div style="text-align: center;"> <img style="width: {captured_number}%;" src="./img/{found_files[0]}"/> </div>'
                processed_content = f'{img_page_file_part_I}{mid}{img_page_file_part_II}'

            chapters.append(processed_content)

        # If there is only one image file, the placement (top, middle, or bottom) is considered,
        # and the HTML content is generated accordingly with appropriate formatting.
        elif len(found_files) == 1:
            processed_content = ''
            parts = found_files[0].split("-")
            captured_word = parts[1]

            captured_number_with_extension = parts[2]
            captured_number = captured_number_with_extension.split(".")[0]

            if captured_word == 'top':

                for i in paragraphs:

                    if not first_line_skipped:
                        first_line_skipped = True
                        processed_content += f"<h6>{i.strip()}</h6>\n"
                        processed_content += f'<div style="text-align: center;"> <img style="width: {captured_number}%;" src="./img/{found_files[0]}" /> </div>'
                        continue
                    i.strip()

                    if i.endswith(".") or re.match(r'^\d', i) or "." in i or "," in i:
                        processed_content += f"<br/><p>{i.strip()}</p><br/>"

                    else:
                        lines = i.splitlines()
                        for l in lines:
                            processed_content += f"<p>{l.strip()}</p>\n"

            elif captured_word == 'middle':
                m_file = []
                for i in paragraphs:

                    if not first_line_skipped:
                        first_line_skipped = True
                        processed_content += f"<h6>{i.strip()}</h6>\n"
                        continue
                    i.strip()

                    if i.endswith(".") or re.match(r'^\d', i) or "." in i or "," in i:
                        processed_content += f"<br/><p>{i.strip()}</p><br/>"

                    else:
                        lines = i.splitlines()
                        for l in lines:
                            processed_content += f"<p>{l.strip()}</p>\n"

                m_file.append(processed_content)
                full_content = ''.join(m_file)

            # Calculate the middle index of the full content
                middle_index = len(full_content) // 2

                img_page_file_part_I = full_content[:middle_index]
                img_page_file_part_II = full_content[middle_index:]
                mid = f'<div style="text-align: center;"> <img style="width: {captured_number}%;" src="./img/{found_files[0]}" /> </div>'
                processed_content = f'{img_page_file_part_I}{mid}{img_page_file_part_II}'

            elif captured_word == 'bottom':

                for i in paragraphs:

                    if not first_line_skipped:
                        first_line_skipped = True
                        processed_content += f"<h6>{i.strip()}</h6>\n"
                        continue
                    i.strip()

                    if i.endswith(".") or re.match(r'^\d', i) or "." in i or "," in i:
                        processed_content += f"<br/><p>{i.strip()}</p><br/>"

                    else:
                        lines = i.splitlines()
                        for l in lines:
                            processed_content += f"<p>{l.strip()}</p>\n"

                processed_content += f'<div style="text-align: center;"> <img style="width: {captured_number}%;" src="./img/{found_files[0]}"  /> </div>'

            chapters.append(processed_content)

        # If the text file doesn't contain any image references, the code proceeds to the next part without generating image-related HTML.
        else:
            processed_content = ''
            for i in paragraphs:
                if not first_line_skipped:
                    first_line_skipped = True
                    processed_content += f"<h6>{i.strip()}</h6>\n"
                    continue
                i.strip()

                if i.endswith(".") or re.match(r'^\d', i) or "." in i or "," in i:
                    processed_content += f"<br/><p>{i.strip()}</p><br/>"

                else:
                    lines = i.splitlines()
                    for l in lines:
                        processed_content += f"<p>{l.strip()}</p>\n"

            chapters.append(processed_content)

else:
    print(f"No .txt files found in the folder '{folder_path}'.")

    print(f"No all.txt files found in the folder '{folder_path}'.")
# -----------------------------------------------------------------------------------------------------------
# processed_content without image
chapters_without_img = []
if all_txt_files:
    for txt_file in all_txt_files:
        file_path = os.path.join(folder_path, txt_file)
        processed_content = ''
        with open(file_path, 'r', encoding='utf-8') as file:
            in_text = file.read()
            paragraphs = in_text.split('\n\n')

            first_line_skipped = False

        for i in paragraphs:
            if not first_line_skipped:
                first_line_skipped = True
                processed_content += f"<h6>{i.strip()}</h6>\n"
                continue
            i.strip()

            if i.endswith(".") or re.match(r'^\d', i) or "." in i or "," in i:
                processed_content += f"<br/><p>{i.strip()}</p><br/>"

            else:
                lines = i.splitlines()
                for l in lines:
                    processed_content += f"<p>{l.strip()}</p>\n"
                    
        chapters_without_img.append(processed_content)



# -----------------------------------------------------------------------------------------------------------
def createEpub(list_chapters,with_image):
    chapters = list_chapters
    # Create an EPUB book
    book = epub.EpubBook()

    # Set metadata
    book.set_title(book_title)
    book.set_language('si')
    book.add_author(author)
    book.add_metadata(None, 'meta', '', {
                      'name': 'cover', 'content': 'cover_image'})

    # set cover image
    try:
        cover_image = epub.EpubItem(uid="cover_image", file_name="cover.jpg", content=open(f"{folder_path}/jpg/0000-cover.jpg", "rb").read())
        book.add_item(cover_image)

        cover_content = f'''
        <div style="text-align: center;">
        <img style="max-width: 100%;" alt="img" src="./img/0000-cover.jpg"/>
        </div>
        <br/>
        <h1>{book_title}</h1>
        <h3>{author}</h3>
        <br/>
        <br/>
        <br/>
        <br/>
        <h2>{sinhala_book_name}</h2>
        <h3>{sinhala_author_name}</h3>
    '''
    except Exception as e:
        cover_content = f'''
        <br/>
        <h1>{book_title}</h1>
        <h3>{author}</h3>
        <br/>
        <br/>
        <br/>
        <br/>
        <h2>{sinhala_book_name}</h2>
        <h3>{sinhala_author_name}</h3>
    '''

    # content of style.css file
    style_content = '''
    @font-face {
        font-family: 'zw';
        src: url(res:///opt/sony/ebook/FONT/zw.ttf),
            url(res:///Data/FONT/zw.ttf),
            url(res:///opt/sony/ebook/FONT/tt0011m_.ttf),
            url(res:///fonts/ttf/zw.ttf),
            url(res:///../../media/mmcblk0p1/fonts/zw.ttf),
            url(res:///DK_System/system/font/zw.ttf),
            url(res:///abook/fonts/zw.ttf),
            url(res:///system/fonts/zw.ttf),
            url(res:///system/media/sdcard/fonts/zw.ttf),
            url(res:///media/fonts/zw.ttf),
            url(res:///sdcard/fonts/zw.ttf),
            url(res:///system/fonts/DroidSansFallback.ttf),
            url(res:///mnt/MOVIFAT/font/zw.ttf),
            url(fonts/zw.ttf);
    }

    @font-face {
        font-family: 'sinhalaFont';
        src: url('https://fonts.googleapis.com/css2?family=Noto+Serif+Sinhala:wght@100..900&display=swap');
    }

    body {
        padding: 0%;
        margin-top: 0%;
        margin-bottom: 0%;
        margin-left: 1%;
        margin-right: 1%;
        line-height: 130%;
        text-align: justify;
        font-family: 'zw', sans-serif; /* Specify the default font */
    }

    p {
        margin: 0px;
        text-indent: 0px;
        line-height: 1.4;
        text-align: justify;
    }

    div {
        margin:0px;
        padding:0px;
        line-height:130%;
        text-align: justify;
    }
    h1 {
        line-height:130%;
        text-align: center;
        font-weight:bold;
        font-size:xx-large;
    }
    h2 {
        line-height:130%;
        text-align: center;
        font-weight:bold;
        font-size:x-large;
    }
    h3 {
        line-height:130%;
        text-align: center;
        font-weight:bold;
        font-size:large;
    }
    h6 {
        line-height:normal;
        text-align: center;
        margin-bottom = 2px;
        padding-bottom: 2px;
    }
    li {
        list-style-type: none;
        line-height: 2
    }
    '''

    toc_list = []

    style = epub.EpubItem(uid="style", file_name="style.css",
                          media_type="text/css", content=style_content)
    book.add_item(style)

    # Add cover image (optional)
    cover_page = epub.EpubHtml(title='Cover', file_name='cover.xhtml')
    cover_page.content = cover_content
    cover_page.add_link(href="style.css", rel="stylesheet", type="text/css")

    book.add_item(cover_page)
    book.spine = [cover_page, 'nav']

    for img_file in all_img_files:
        file_path = os.path.join(img_folder_path, img_file)
        image = epub.EpubItem(uid=f"{img_file}", file_name=f"img/{img_file}", content=open(f"{file_path}", "rb").read())
        book.add_item(image)

    for index, chap in enumerate(chapters):
        chapter = epub.EpubHtml(title=f'Chapter {index + 1}', file_name=f'{all_txt_files[index]}.xhtml')
        chapter.content = chap
        book.add_item(chapter)
        book.spine.append(chapter)
        chapter.add_link(href="style.css", rel="stylesheet", type="text/css")

    for i, chap_h in enumerate(chapter_head):
        toc_list.append(epub.Link(f'{chap_h}.xhtml', f'පරිච්ඡේදය { i + 1}', f'chapter_{i + 1}'))

    book.toc = tuple(toc_list)

    # Add NCX and Navigation items
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.get_item_with_id('nav').add_link(href="style.css", rel="stylesheet", type="text/css")

    if not with_image :
        epub.write_epub(f'{DestFolder}/{last_part}-NoImages.epub', book)
        print(f'{DestFolder}/{last_part}-NoImages.epub')
    else:
        epub.write_epub(f'{DestFolder}/{last_part}.epub', book)
        print(f'{DestFolder}/{last_part}.epub')
        
    logging.info(f'input folderpath = {SrcFolder}')
    logging.info(f'output folderpath = {DestFolder}')
    logging.info(f'book titel = {book_title}')
    logging.info(f'book author = {author}')
    logging.info(f'ebook output = {DestFolder}/{last_part}.epub')

createEpub(chapters_without_img,False)
createEpub(chapters,True)
