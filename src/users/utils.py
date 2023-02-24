import re

from core.exceptions import GeneralPhoneNumberError


def phone_number_validators(value):
    number = re.compile(r"^(?:\+?996)?\d{9}$")
    if not number.search(value):
        raise GeneralPhoneNumberError()
