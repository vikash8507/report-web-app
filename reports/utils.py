import base64, uuid
from re import I
from django.core.files.base import ContentFile

def get_rep_image_path(image):
    _, str_img = image.split(';base64')
    decoded_img = base64.b64decode(str_img)
    img_name = str(uuid.uuid4())[:10] + '.png'
    data = ContentFile(decoded_img, name = img_name)

    return data