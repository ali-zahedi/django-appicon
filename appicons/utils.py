import mimetypes
import random

from django.utils.timezone import now


def get_document_path(instance, filename):
    mime = instance.file.file.content_type
    guess_extension = mimetypes.guess_extension(mime)
    if guess_extension:
        guess_extension = guess_extension[1:]
    else:
        guess_extension = filename.split(".")[-1][-5:]
    name = 'icons/{0}-{1}.{2}'.format(
        now().strftime('%y-%m-%d-%H-%M-%S'),
        random.randint(0, 10000),
        guess_extension
    )
    return name

