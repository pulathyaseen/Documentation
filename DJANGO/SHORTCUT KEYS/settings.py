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
        'keys': 'n + t ',  # go to create transaction
        'link': '/app/finance/create-transaction'
    },
]
SPECIAL_DISABLED = True
# END keyboard_shortcuts settings #

...
