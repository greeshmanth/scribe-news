from ebooklib import epub
import newspaper
import requests
from bs4 import BeautifulSoup
import utils
from datetime import date

# Step 1: Fetch the RSS feed
#rss_url = ""  # Replace with your RSS feed URL
rss_urls = [
    ("Detusche Welle","https://rss.dw.com/rdf/rss-en-top"),
    ("BBC","https://feeds.bbci.co.uk/news/world/rss.xml"),
    ("The Guardian", "https://www.theguardian.com/world/rss"),
    ("The New Yorker","https://www.newyorker.com/feed/everything"),
    ("Die Zeit","https://newsfeed.zeit.de/english/index")
]

urls = utils.get_articles_from_feeds(rss_urls,10)
utils.get_new_cover_image()
utils.edit_cover()

# Create a new book
book = epub.EpubBook()

# Set metadata
book.set_title("News - " +  date.today().strftime("%B %d, %Y"))
book.set_language("en")
book.add_author("Greeshmanth Koganti")
book.toc = []
book.spine = ["nav"]

# Add cover image
with open("cover.jpg", "rb") as cover_file:
    cover = cover_file.read()
book.set_cover("cover.jpg", cover)

for source, url_list in urls:

    chapters = []

    for index, url in enumerate(url_list):

        article = newspaper.article(url)
        title = article.title.split(" – DW")[0]
        text = article.text.replace("\n", "<br>")

        print(title)

        chapter = epub.EpubHtml(title=title, file_name=source+str(index)+".xhtml", lang="en")
        chapter.content = "<h1>" + title + "</h1><p>" + text + "</p>"

        # Add chapter to book
        book.add_item(chapter)

        chapters.append(chapter)
        book.spine.append(chapter)

    # Define Table of Contents explicitly
    book.toc.append((epub.Section(source), chapters))
    
# Add navigation files
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# Save the book as an EPUB file
filepath = date.today().strftime("news-%Y-%m-%d.epub")
epub.write_epub(filepath, book, {})
print("EPUB created successfully!")
utils.send_mail_to_kindle(filepath)












