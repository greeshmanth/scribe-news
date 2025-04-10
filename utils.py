import requests
from bs4 import BeautifulSoup
import resend
import base64
from PIL import Image, ImageDraw, ImageFont
from datetime import date

def get_articles_from_feeds(rss_urls, count = 10):
    urls = []

    for source, rss_url in rss_urls:
        response = requests.get(rss_url)

        # Step 2: Parse the feed using Beautiful Soup
        soup = BeautifulSoup(response.content, 'xml')  # Use 'xml' parser for RSS feeds

        # Step 3: Extract items from the feed
        items = soup.find_all('item')  # Find all <item> tags


        loop_urls = []
        # Step 4: Iterate through the items and print details
        for item in items[:count]:
            loop_urls.append(item.find('link').text)  # Extract <link> content

        urls.append((source, loop_urls))    

    return urls

def get_new_cover_image(filename="cover.jpg"):
    # Send a request to the URL
    response = requests.get("https://picsum.photos/1600/2560/?grayscale")

    # Save the image
    with open("cover.jpg", "wb") as file:
        file.write(response.content)

    print("Image downloaded successfully!")

def send_mail_to_kindle(file_path = "news.epub"):

    resend.api_key = "re_PYuK9JVV_425azDhwRKa5cMDGWqXPPpfW"

    # Read the file and encode it in Base64
    with open(file_path, "rb") as f:
        attachment_content = base64.b64encode(f.read()).decode("utf-8")  # Proper encoding

    params: resend.Emails.SendParams = {
        "from": "Greeshmanth Koganti <greeshmanth@weiko.org>",
        "to": ["rg_OtPfEh@kindle.com"],
        "subject": "News",
        "html": "News",
        "attachments" : [
            {
                "content": attachment_content,
                "filename": file_path,
            }
        ]
    }

    email = resend.Emails.send(params)
    print(email)

def edit_cover(filename="cover.jpg"):
    # Load the image
    image = Image.open(filename)

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # ...
    # Define the text properties
    font = ImageFont.truetype("Coolvetica Rg.otf", 144)
    position = (50, 50)

    # Define text
    text = date.today().strftime("%B %d")

    # Get text bounding box (to calculate text dimensions)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]  # Width
    text_height = bbox[3] - bbox[1]  # Height

    # Calculate centered position
    image_width, image_height = (1600, 2560)
    x = (image_width - text_width) // 2
    y = (image_height - text_height) // 2

    # Define the box position and color
    white_color = (255, 255, 255)  # RGB for white
    box_position = [(0, 0), (1600, text_height*2)]  # Top-left and bottom-right corners

    # Draw the rectangle (white box)
    transparent_color = (0, 0, 0, 100)  # Black with 100/255 transparency (adjust as needed)
    draw.rectangle(box_position, fill=255)

    # Draw text at the centered position
    draw.text((x, 50), text, font=font, fill='black')

    # Save or display the modified image
    image.save(filename)