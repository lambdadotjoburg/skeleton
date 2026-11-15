from .validate import Rules

from .rules.required import required
from .rules.version import version
from .rules.package import package_name
from .rules.identifier import identifier
from .rules.date import iso_date
from .rules.license import license
from .rules.url import url_prefix

METADATA_RULES: Rules = {

    "profile": [
        required,
    ],

    "name": [
        required,
        package_name,
    ],

    "title": [
        required,
    ],

    "version": [
        required,
        version,
    ],

    "author": [
        required,
    ],

    "description": [
        required,
    ],

    "license": [
        required,
        license,
    ],
}

INIT_RULES: Rules = {
    
    **METADATA_RULES,

    # "ws": [
    #     required,
    #     url_prefix,
    # ],

    "api": [
        required,
        url_prefix,
    ],

    "app": [
        required,
        identifier
    ],

    "date": [
        required,
        iso_date
    ],
}