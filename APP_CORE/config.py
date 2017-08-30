# application config

# put things like, app name, version, and other default config here
_KEYS = {
    'appname'   :   'DJ',
    'version'   :   '0.0.1',
}

# put all sort of labels here
_LABELS = {
    'btn.admin'         : 'Admin',
    'btn.logout'        : 'Logout',
    'btn.signup'        : 'Signup',
    'title.signup'      : 'Member Registration',
    'form.username'     : 'username',
    'form.password'     : 'password',
    'msg.auth.fail'     : 'Your username or password is not correct, try again?',
}

def key(key):
    try: return _KEYS[key]
    except Exception: return None

def label(key):
    try: return _LABELS[key]
    except Exception: return None
