import logging


def convert_pk(model, x):
    try:
        i = model._meta.pk.to_python(x)
        return i
    except:
        logging.debug(f"Cant convert pk {x}")
        return None
