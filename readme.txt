EpubCreate - Convert Sinhala Text to EPUB

Introduction:

This script is designed to create EPUB files from Sinhala Unicode text files. It organizes the content into chapters,handles      cover images, and includes optional images within the text. The generated EPUB can be tested on Android and Apple ebook readers.

System Requirements:

Python 3
EbookLib library (`pip install EbookLib`)

Usage Instructions:

Open a command prompt or terminal.
Navigate to the script directory:
Example: cd C:\tmp\Avishka\EpubCreate\scripts
Run the script with two parameters:
python EpubCreate.py <SrcFolder> <DestFolder>

Example Usage:

C:\Python311>python scripts\EpubCreate.py <SrcFolder> <DestFolder>

EXplanation of Parameters:

<SrcFolder>: The path to the folder containing your Sinhala Unicode text files.
<DestFolder> (Optional): The path where you want the generated EPUB file to be saved. If not provided, the "output" folder will   be created within the source folder.

Relative paths:
C:\Python311\python scripts\EpubCreate.py input\Adyathana2(WasanthaKKGee)-SamudraW output1
C:\Python311\python scripts\EpubCreate.py input\DoltonGiithaNir-NayanaSR output1
C:\Python311\python scripts\EpubCreate.py input\DharmasiriGamage-RanjithA output1

Absolute paths:
python EpubCreate.py c:\tmp\input\Adyathana2(WasanthaKKGee)-SamudraW d:\tmp2\output2
Creating EPUB with default destination:
python EpubCreate.py c:\tmp\input\Adyathana2(WasanthaKKGee)-SamudraW

If you want to add an image for the book, please follow these instructions:

1. Create a folder named "img" within your book's input folder.
   Example: input\Adyathana2(WasanthaKKGee)-SamudraW\jpg

2. Rename your image files using the following format:
   Format: <image-position>-<image-size>.<file-extension>
   Example:
   - 001b-top-25.jpg
   - 001b-middle-75.jpeg
   - 001b-bottom-100.png

Note: The author's name and book title in Sinhala language are captured from the 1st line and 3rd line of the first .txt file.

Supported/Tested Devices/App:
Apple:
Devices/App:

iPhone
Books app
Instructions:
To send from WhatsApp, use the upload button (top right) and select Books app.

Android:
Epub Reader Apps:
Epub reader for all
Pocket Reader

Kindle:
Device:
Amazon Kindle
