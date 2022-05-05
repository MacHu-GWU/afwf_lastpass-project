# -*- coding: utf-8 -*-

from typing import List
import enum
import subprocess

import afwf
from pathlib_mate import Path

from .paths import path_name_txt


class PasswordForm(enum.Enum):
    name = "name"
    folder = "folder"
    fullname = "fullname"
    username = "Username"
    password = "Password"
    url = "URL"
    notes = "Notes"


class SecureNoteForm(enum.Enum):
    name = "name"
    folder = "folder"
    fullname = "fullname"
    url = "URL"
    notes = "Notes"


class AddressForm(enum.Enum):
    fax = "Fax"
    mobile_phone = "Mobile Phone"
    evening_phone = "Evening Phone"
    phone = "Phone"
    email_address = "Email Address"
    timezone = "Timezone"
    country = "Country"
    zip_postal_code = "Zip / Postal Code"
    state = "State"
    county = "County"
    city_town = "City / Town"
    address_3 = "Address 3"
    address_2 = "Address 2"
    address_1 = "Address 1"
    company = "Company"
    birthday = "Birthday"
    gender = "Gender"
    last_name = "Last Name"
    middle_name = "Middle Name"
    first_name = "First Name"
    title = "Title"
    language = "Language"
    note_type = "NoteType"
    notes = "Notes"


class PaymentCardForm(enum.Enum):
    name = "name"
    folder = "folder"
    fullname = "fullname"
    number = "Number"
    name_on_card = "Name on Card"
    security_code = "Security Code"
    expiration_date = "Expiration Date"
    start_date = "Start Date"
    type = "Type"
    language = "Language"
    note_type = "NoteType"
    notes = "Notes"


class BankAccounts(enum.Enum):
    name = "name"
    folder = "folder"
    fullname = "fullname"
    branch_phone = "Branch Phone"
    branch_address = "Branch Address"
    account_number = "Account Number"
    routing_number = "Routing Number"
    pin = "Pin"
    iban_number = "IBAN Number"
    swift_code = "SWIFT Code"
    account_type = "Account Type"
    bank_name = "Bank Name"
    language = "Language"
    note_type = "NoteType"
    notes = "Notes"


def parse_output(name: str, output: str) -> dict:
    data = dict()

    lines = output.split("\n")

    fullname = lines[0].split("[id")[0].strip()
    folder = fullname[::-1].replace(name[::-1], "")[::-1]

    data["name"] = name
    data["folder"] = folder
    data["fullname"] = fullname

    for line in lines[1:]:
        try:
            key, value = line.split(": ", 1)
            data[key.strip()] = value.strip()
        except:
            pass

    processed_data = {
        k: v
        for k, v in data.items()
        if not (
            (k.lower() in data) and (k.lower() != k)
        )
    }

    return processed_data


def show(name: str) -> dict:
    response = subprocess.check_output([
        "lpass", "show", name,
    ]).decode("utf-8")
    return parse_output(name, response)


def parse_name_txt(path: Path = path_name_txt) -> List[str]:
    return [
        line.strip()
        for line in path.read_text().strip().split("\n")
        if line.strip()
    ]
