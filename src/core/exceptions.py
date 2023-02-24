from typing import Optional
from typing import Union

from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def _flatten(details: Union[list, dict, str], field_errors) -> None:
    # TODO: fix nested errors
    if isinstance(details, dict):
        for key, detail in details.items():
            field_errors.append({"field": key, "message": str(detail[0].get("message"))})


def flat_field_errors(details: Union[list, dict, str]) -> list[dict]:
    field_errors = []
    _flatten(details, field_errors)
    return field_errors


def drf_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, Http404):
        return Response(
            {
                "code": GeneralNotFound.code,
                "message": GeneralNotFound.message,
                "field_errors": [],
            },
            status=GeneralNotFound.http_code,
        )
    if isinstance(exc, ValidationError):
        # TODO: fix several error cases
        #  1. object in object
        #  2. list in object
        return Response(
            {
                "code": GeneralValidationError.code,
                "message": GeneralValidationError.message,
                "field_errors": flat_field_errors(exc.get_full_details()),
            },
            status=exc.status_code,
        )
    if isinstance(exc, APIException):
        return Response(
            {
                "code": GeneralBadRequest.code,
                "message": str(exc),
                "field_errors": [],
            },
            status=exc.status_code,
        )
    if isinstance(exc, GeneralBaseException):
        return Response(
            {
                "code": exc.code,
                "message": exc.message,
                "field_errors": [],
            },
            status=exc.http_code,
        )

    return response  # noqa: R504


class GeneralBaseException(Exception):
    code = "UnexpectedException"
    message = "Unexpected error occurred while processing your request"
    http_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    field_errors = []

    def __init__(
        self,
        message: str = "",
        code: str = "",
        http_code: Optional[int] = None,
        field_errors: Optional[list] = None,
    ):
        self.code = code or self.code
        self.message = message or self.message
        self.http_code = http_code or self.http_code
        self.field_errors = field_errors or self.field_errors


class GeneralValidationError(GeneralBaseException):
    code = "ValidationError"
    message = "Validation error"
    http_code = status.HTTP_400_BAD_REQUEST


class GeneralNotFound(GeneralBaseException):
    code = "ObjectDoesNotExist"
    message = "Object does not exist"
    http_code = status.HTTP_404_NOT_FOUND


class GeneralUserNotFound(GeneralNotFound):
    code = "UserDoesNotExist"
    message = "User does not exist"


class GeneralUserAlreadyExist(GeneralBaseException):
    code = "UserAlreadyExist"
    message = "User already exist"
    http_code = status.HTTP_409_CONFLICT


class GeneralBadRequest(GeneralBaseException):
    code = "BadRequest"
    message = "Bad request"
    http_code = status.HTTP_400_BAD_REQUEST


class GeneralPermissionDenied(GeneralBaseException):
    code = "PermissionDenied"
    message = "Permission denied"
    http_code = status.HTTP_403_FORBIDDEN


class GeneralUnauthorized(GeneralBaseException):
    code = "Unauthorized"
    message = "Unauthorized"
    http_code = status.HTTP_401_UNAUTHORIZED


class GeneralFirebaseError(GeneralBaseException):
    code = "InvalidToken"
    message = "Invalid token"
    http_code = status.HTTP_400_BAD_REQUEST


class GeneralPhoneNumberError(GeneralBaseException):
    code = "IncorrectPhoneNumber"
    message = "Incorrect phone number"
    http_code = status.HTTP_400_BAD_REQUEST


class GeneralAuthenticationFailed(GeneralBaseException):
    code = "InvalidLoginOrPassword"
    message = "Неправильный логин или пароль"
    http_code = status.HTTP_401_UNAUTHORIZED


class GeneralWrongStatusTransitionError(GeneralBaseException):
    code = "WrongStatusTransition"
    message = "Wrong status transition"
    http_code = status.HTTP_400_BAD_REQUEST
