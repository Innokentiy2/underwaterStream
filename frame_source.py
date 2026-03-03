from PIL import Image, ImageDraw
import io, time

def generate_frame():
    img = Image.new("RGB", (640, 480), (0, 20, 60))
    draw = ImageDraw.Draw(img)
    t = time.strftime("%H:%M:%S")
    text = f"Underwater demo (no camera)\n{t}"
    draw.text((20, 20), text, fill=(200, 230, 255))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()
