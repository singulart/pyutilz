from ebooklib import epub

# Create an EPUB book
book = epub.EpubBook()
book.set_identifier('123456')
book.set_title('Untitled')
book.set_language('en')
book.add_author('Unknown')

# Set the cover image (some Kindle devices require it explicitly added as an item)
with open("brod.jpg", 'rb') as cover_file:
    cover_data = cover_file.read()

book.set_cover("cover.jpg", cover_data)

# Add the cover as a separate EPUB item (for Kindle support)
cover_item = epub.EpubItem(
    uid="cover",
    file_name="image_cover.xhtml",
    media_type="application/xhtml+xml",
    content=f'''<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <title>Cover</title>
        </head>
        <body>
            <img src="cover.jpg" alt="Cover Image" style="width:100%; height:auto;"/>
        </body>
    </html>'''
)

book.add_item(cover_item)

# Add a valid minimal XHTML content file (required for EPUB validation)
empty_chapter = epub.EpubHtml(title='Blank', file_name='blank.xhtml', lang='en')
empty_chapter.content = '''
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <title>Blank</title>
        </head>
        <body>
            <p>This is a blank page.</p>
        </body>
    </html>
'''

book.add_item(empty_chapter)

# Ensure the cover is included in the spine and guide
book.spine = ['cover', 'nav', empty_chapter]
book.guide = [{'type': 'cover', 'title': 'Cover', 'href': 'image_cover.xhtml'}]

# Add navigation (EPUB3 requirement)
nav = epub.EpubNav()
book.add_item(nav)

# Write the EPUB file
epub.write_epub('empty_book.epub', book, {})

print("EPUB file 'empty_book.epub' created successfully with Kindle-compatible cover.")

