INSTALLED_APPS = [
    ...
    'keyboard_shortcuts',
    ...
]

...


# START keyboard_shortcuts settings #
HOTKEYS = [
    {
        'keys': 'g + h',  # go home
        'link': '/'
    },
    {
        'keys': 'n + p',  # go to patient registration
        'link': '/app/patients/create-registration'
    },
    {
        'keys': 'n + p + r',  # go to create patient receipt
        'link': '/app/finance/create-patient-receipt'
    },
    {
        'keys': 'n + t ',  # go to create transaction
        'link': '/app/finance/create-transaction'
    },
    {
        'keys': 'r + d',  # go to reffer to dr
        'link': '/app/doctors/create-refer-doctor'
    },
]
SPECIAL_DISABLED = True
# END keyboard_shortcuts settings #

...
