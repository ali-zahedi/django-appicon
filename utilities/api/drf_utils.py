"""
Sometimes in your Django model you want to raise a ``ValidationError`` in the ``save`` method, for
some reason.
This exception is not managed by Django Rest Framework because it occurs after its validation
process. So at the end, you'll have a 500.
Correcting this is as simple as overriding the exception handler, by converting the Django
``ValidationError`` to a DRF one.
"""
import logging

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.exceptions import ValidationError

LOG = logging.getLogger(__name__)


def exception_handler(exception, context):
    """Handle Django ValidationError as an accepted exception
    Must be set in settings:
    For the parameters, see ``exception_handler``
    """

    if isinstance(exception, DjangoValidationError):
        if hasattr(exception, "message_dict"):
            detail = exception.message_dict
        elif hasattr(exception, "message"):
            detail = exception.message
        elif hasattr(exception, "messages"):
            detail = exception.messages
        else:
            LOG.error("BAD VALIDATION MESSAGE: %s", exception)
        exception = ValidationError(detail=detail)

    return drf_exception_handler(exception, context)
