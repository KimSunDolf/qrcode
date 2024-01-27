from flask import Flask, render_template, request, redirect, url_for
import qrcode
from PIL import Image as PILImage
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qrcode', methods=['POST'])
def generate_qrcode():
    data = request.form.get('text')
    icon = request.files.get('icon')

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Add icon
    if icon:
        
        icon_img = PILImage.open(icon)
        qr_img.paste(icon_img, (int((qr_img.size[0] - icon_img.size[0]) / 2), int((qr_img.size[1] - icon_img.size[1]) / 2)))

    # Save or return the image
    img_io = BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return img_io.getvalue(), 200, {'Content-Type': 'image/png'}

if __name__ == '__main__':
    app.run(debug=True)
