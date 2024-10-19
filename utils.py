import os
import uuid
import base64
from magic import Magic
from werkzeug.utils import secure_filename
from typing import (
    Dict,
    Optional
)


def convert_image_to_base64(image_path: str) -> Optional[Dict[str, str]]:
    if image_path and  os.path.exists(image_path):
        with open(image_path, 'rb') as image:
            image_binary = image.read()

            image_base64 = base64.b64encode(image_binary).decode('utf-8')
            mime = Magic(mime=True)
            mime_type = mime.from_file(image_path)

            return {
                'image_base64': image_base64,
                'mime_type': mime_type
            }

    return None


def save_image(image: str,
               path: str = 'alxconnect/static/uploads/images') -> Optional[str]:
    if not os.path.exists(path):
        os.makedirs(path)

    f_name = image.filename
    if image and f_name:
        filename = str(uuid.uuid4()) + secure_filename(f_name)
        profile_picture_url = os.path.join(path, filename)
        image.save(profile_picture_url)

        return profile_picture_url

    return None
