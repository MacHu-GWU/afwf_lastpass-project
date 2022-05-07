# -*- coding: utf-8 -*-

from typing import List
import enum
import subprocess
from collections import OrderedDict

import afwf
from pathlib_mate import Path

from .paths import (
    lasspass_cli,
    path_name_txt,
)
from . import images


class PasswordForm(enum.Enum):
    name = "name"
    folder = "folder"
    fullname = "fullname"
    username = "username"
    password = "password"
    username_field = "username-field"
    password_field = "password-field"
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


class DriversLicenseForm(enum.Enum):
    height = "Height"
    sex = "Sex"
    birth = "Birth"
    country = "Country"
    code = "Code"
    state = "State"
    town = "Town"
    address = "Address"
    name = "Name"
    class_ = "Class"
    date = "Date"
    number = "Number"
    language = "Language"
    note_type = "NoteType"
    notes = "Notes"


class PassportForm(enum.Enum):
    expiration_date = "Expiration Date"
    issued_date = "Issued Date"
    date_of_birth = "Date of Birth"
    issuing_authority = "Issuing Authority"
    nationality = "Nationality"
    sex = "Sex"
    number = "Number"
    country = "Country"
    name = "Name"
    type = "Type"
    language = "Language"
    note_type = "NoteType"
    notes = "Notes"


class SSNForm(enum.Enum):
    number = "Number"
    name = "Name"
    note_type = "NoteType"
    notes = "Notes"


class DatabaseForm(enum.Enum):
    name = "name"
    folder = "folder"
    fullname = "fullname"
    username = "Username"
    password = "Password"
    alias = "Alias"
    sid = "SID"
    database = "Database"
    port = "Port"
    hostname = "Hostname"
    type = "Type"
    note_type = "NoteType"
    notes = "Notes"


class ServerForm(enum.Enum):
    name = "name"
    folder = "folder"
    fullname = "fullname"
    username = "Username"
    password = "Password"
    hostname = "Hostname"
    language = "Language"
    note_type = "NoteType"
    notes = "Notes"


class SSHForm(enum.Enum):
    name = "name"
    folder = "folder"
    fullname = "fullname"
    date = "Date"
    hostname = "Hostname"
    public_key = "Public Key"
    private_key = "Private Key"
    passphrase = "Passphrase"
    format = "Format"
    bit_strength = "Bit Strength"
    language = "Language"
    note_type = "NoteType"
    notes = "Notes"


class SoftwareLicenseForm(enum.Enum):
    name = "name"
    folder = "folder"
    fullname = "fullname"
    order_total = "Order_Total"
    number_of_licenses = "Number_of_Licenses"
    order_number = "Order_Number"
    purchase_date = "Purchase_Date"
    price = "Price"
    website = "Website"
    support_email = "Support_Email"
    publisher = "Publisher"
    version = "Version"
    licensee = "Licensee"
    license_key = "License_Key"
    note_type = "NoteType"
    notes = "Notes"


def mask_password(v) -> str:
    return "***"


def mask_card_number(v) -> str:
    return f"***{v[-4::]}"


def mask_bank_account_number(v) -> str:
    return f"{v[::3]}***{v[-3::]}"


sensitive_fields: dict = {
    PasswordForm.password.value: mask_password,
    PasswordForm.password_field.value: mask_password,
    PaymentCardForm.number.value: mask_card_number,
    PaymentCardForm.security_code.value: mask_password,
    BankAccounts.account_number.value: mask_bank_account_number,
    BankAccounts.pin.value: mask_password,
    DriversLicenseForm.number.number: mask_bank_account_number,
    DatabaseForm.password.value: mask_password,
    SSHForm.private_key.value: mask_password,
}

_all_fields = []
_all_fields.extend([v.value for v in PasswordForm.__members__.values()])
_all_fields.extend([v.value for v in SecureNoteForm.__members__.values()])
_all_fields.extend([v.value for v in AddressForm.__members__.values()])
_all_fields.extend([v.value for v in PaymentCardForm.__members__.values()])
_all_fields.extend([v.value for v in BankAccounts.__members__.values()])
_all_fields.extend([v.value for v in DriversLicenseForm.__members__.values()])
_all_fields.extend([v.value for v in PassportForm.__members__.values()])
_all_fields.extend([v.value for v in SSNForm.__members__.values()])
_all_fields.extend([v.value for v in DatabaseForm.__members__.values()])
_all_fields.extend([v.value for v in ServerForm.__members__.values()])
_all_fields.extend([v.value for v in SSHForm.__members__.values()])
_all_fields.extend([v.value for v in SoftwareLicenseForm.__members__.values()])
all_fields = set(_all_fields)


def parse_output(name: str, output: str) -> dict:
    """
    'name' is always the first field
    """
    data = OrderedDict()

    lines = output.split("\n")

    fullname = lines[0].split("[id")[0].strip()
    folder = fullname[::-1].replace(name[::-1], "")[::-1]

    data["name"] = [name, ]
    data["folder"] = [folder, ]
    data["fullname"] = [fullname, ]

    previous_key = ""
    data[""] = []
    for line in lines[1:]:
        if ": " in line:
            key, value = line.split(": ", 1)
            key, value = key.strip(), value
            if key in all_fields:
                data[key] = [value, ]
                previous_key = key
            else:
                data[previous_key].append(line)
        else:
            data[previous_key].append(line)
    _ = data.pop("")

    processed_data = OrderedDict([
        (k, "\n".join(v))
        for k, v in data.items()
        if not (
            (k.lower() in data) and (k.lower() != k)
        )
    ])

    return processed_data


def show(name: str) -> dict:
    response = subprocess.check_output([
        lasspass_cli, "show", name,
    ]).decode("utf-8")
    return parse_output(name, response)


def parse_name_txt(path: Path = path_name_txt) -> List[str]:
    return list(set([
        line.strip()
        for line in path.read_text().strip().split("\n")
        if line.strip()
    ]))


def password_name_to_items(name: str) -> List[afwf.Item]:
    data = show(name)
    item_list = list()
    for k, v in data.items():
        if k in sensitive_fields:
            title = f"{k} = {sensitive_fields[k](v)}"
        else:
            title = f"{k} = {v}"
        item = afwf.Item(
            title=title,
            subtitle="",
            autocomplete=f"{name}@@{k}",
            arg=v,
            icon=afwf.Icon.from_image_file(images.lastpass),
            variables={"field": k},
        )
        # Since name is always on top, add special functionality to it
        if k == PasswordForm.name.value:
            if PasswordForm.password.value in data:
                secure_value = data[PasswordForm.password.value]
            elif SecureNoteForm.notes.value in data:
                secure_value = data[SecureNoteForm.notes.value]
            elif DatabaseForm.password.value in data:
                secure_value = data[DatabaseForm.notes.value]
            else:
                secure_value = v
            item.subtitle = "hit 'enter' to ENTER the secret"
            item.text = afwf.Text(
                largetype="\n".join([
                    f"{k} = {v}"
                    for k, v in data.items()
                ])
            )
            item.variables["run_apple_script"] = afwf.VarValueEnum.y.value
            item.variables["run_apple_script_arg"] = secure_value

            item.add_modifier(
                mod=afwf.ModEnum.cmd.value,
                subtitle="hit 'CMN + enter' to COPY the secret",
                arg=secure_value,
            )
            if PasswordForm.url.value in data:
                item.add_modifier(
                    mod=afwf.ModEnum.alt.value,
                    subtitle="hit 'Alt + enter' to OPEN the url",
                    arg=data[PasswordForm.url.value],
                )

        elif k == PasswordForm.url.value:
            item.open_url(url=v)
        item_list.append(item)

    return item_list
