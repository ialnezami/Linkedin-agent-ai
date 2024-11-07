from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import textwrap
import random
import os

class SlideGenerator:
    def __init__(self, font_path="arial.ttf", slide_size=(800, 600)):
        self.font_path = font_path
        self.slide_size = slide_size

    def create_slide_image(self, slide_text, slide_title="My Slide Title"):
        """Creates a basic slide with a title and wrapped text content."""
        img = Image.new('RGB', self.slide_size, color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        # Load fonts
        try:
            font_title = ImageFont.truetype(self.font_path, 40)
            font_text = ImageFont.truetype(self.font_path, 30)
        except IOError:
            font_title = ImageFont.load_default()
            font_text = ImageFont.load_default()

        # Title positioning
        title_bbox = draw.textbbox((0, 0), slide_title, font=font_title)
        title_x = (self.slide_size[0] - (title_bbox[2] - title_bbox[0])) // 2
        draw.text((title_x, 20), slide_title, font=font_title, fill=(0, 0, 0))

        # Wrap text for content
        wrapper = textwrap.TextWrapper(width=40)
        wrapped_text = wrapper.fill(text=slide_text)
        draw.multiline_text((40, 100), wrapped_text, font=font_text, fill=(0, 0, 0), spacing=10)

        return img

    def create_stylized_slide(self, slide_text, slide_title="Stylized Slide", slide_number=1):
        """Creates a stylized slide with background circles and a slide number badge."""
        img = Image.new('RGB', self.slide_size, color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        # Load fonts
        try:
            font_title = ImageFont.truetype(self.font_path, 60)
            font_subtitle = ImageFont.truetype(self.font_path, 30)
            font_number = ImageFont.truetype(self.font_path, 30)
        except IOError:
            font_title = ImageFont.load_default()
            font_subtitle = ImageFont.load_default()
            font_number = ImageFont.load_default()

        # Draw background circles
        for _ in range(10):
            radius = random.randint(40, 150)
            x = random.randint(-50, self.slide_size[0] - radius)
            y = random.randint(-50, self.slide_size[1] - radius)
            if random.choice([True, False]):
                draw.ellipse([x, y, x + radius, y + radius], fill=(240, 240, 255))
            else:
                draw.ellipse([x, y, x + radius, y + radius], outline=(180, 180, 200), width=4)

        # Draw slide number badge
        badge_radius = 30
        badge_x, badge_y = 40, 40
        draw.ellipse([badge_x, badge_y, badge_x + badge_radius * 2, badge_y + badge_radius * 2], fill=(100, 100, 120))
        text_bbox = draw.textbbox((0, 0), str(slide_number), font=font_number)
        text_x = badge_x + badge_radius - text_bbox[2] // 2
        text_y = badge_y + badge_radius - text_bbox[3] // 2
        draw.text((text_x, text_y), str(slide_number), font=font_number, fill=(255, 255, 255))

        # Title text
        title_bbox = draw.textbbox((0, 0), slide_title, font=font_title)
        title_x = self.slide_size[0] // 2 - title_bbox[2] // 2
        draw.text((title_x, self.slide_size[1] // 2 - 50), slide_title, font=font_title, fill=(60, 60, 180))

        # Subtitle text
        subtitle_x = self.slide_size[0] // 2 - draw.textbbox((0, 0), slide_text, font=font_subtitle)[2] // 2
        draw.text((subtitle_x, self.slide_size[1] // 2 + 50), slide_text, font=font_subtitle, fill=(120, 120, 120))

        return img


class PDFCarousel:
    def __init__(self, output_pdf="carousel_slides.pdf"):
        self.output_pdf = output_pdf
        self.temp_images = []

    def add_slide(self, slide_image):
        """Saves a slide image temporarily and adds it to the list of images for the PDF."""
        temp_image_path = f"temp_slide_{len(self.temp_images)}.png"
        slide_image.save(temp_image_path)
        self.temp_images.append(temp_image_path)

    def create_pdf(self):
        """Creates a PDF from the list of slide images."""
        c = canvas.Canvas(self.output_pdf, pagesize=A4)
        width, height = A4

        for temp_image_path in self.temp_images:
            # Load image and resize to fit A4 width
            img = Image.open(temp_image_path)
            img = img.resize((int(width), int(width * img.size[1] / img.size[0])))

            # Save the resized image to a temporary path to use in the PDF
            resized_image_path = f"resized_{os.path.basename(temp_image_path)}"
            img.save(resized_image_path)

            # Draw image on PDF
            c.drawImage(resized_image_path, 0, height - img.size[1], width=width, height=img.size[1])
            c.showPage()  # Move to the next page for the next slide

            # Remove resized image
            os.remove(resized_image_path)

        # Save and cleanup
        c.save()
        for temp_image_path in self.temp_images:
            os.remove(temp_image_path)
        self.temp_images.clear()


# Example Usage
slide_generator = SlideGenerator(font_path="arial.ttf")
pdf_carousel = PDFCarousel("carousel_slides.pdf")

# Generate and add slides to the PDF
slide_texts = [
    "Welcome to our LinkedIn Carousel! Slide 1 Content goes here...",
    "Slide 2 Content: Here’s some more information...",
    "Slide 3 Content: Final thoughts and call-to-action!",
]

for i, text in enumerate(slide_texts):
    slide = slide_generator.create_stylized_slide(text, slide_title=f"Slide {i+1}", slide_number=i+1)
    pdf_carousel.add_slide(slide)

# Create the PDF carousel
pdf_carousel.create_pdf()
