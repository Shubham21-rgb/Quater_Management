
#############################
import qrcode
from PIL import Image

# Load and resize logo with LANCZOS
logo = Image.open('static/IITM.png')
basewidth = 100
wpercent = basewidth / logo.width
hsize = int(logo.height * wpercent)
logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)

# Create QR code (high error correction)
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
qr.add_data('https://www.linkedin.com/in/shubham-chakraborty-53974a278?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app')
qr.make(fit=True)

qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

# Center and paste the logo
pos = ((qr_img.width - logo.width) // 2, (qr_img.height - logo.height) // 2)
qr_img.paste(logo, pos, logo if logo.mode == 'RGBA' else None)

qr_img.save('Linked.png')
