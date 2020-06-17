# Note this will not override existing environment settings
from dotenv import load_dotenv
import os

load_dotenv()

def file_must_exist(f):
    if os.path.exists(f): return
    msg = f + " not found."
    try: 
        raise FileNotFoundError(msg)
    except:
        raise IOError(msg)

class Config(object):
    """ Read environment here to create configuration data. """

    # Config.LMUTIL will be a list of args to pass to subprocess.

    _LMUTIL = os.environ.get('LMUTIL')
    if _LMUTIL:
        file_must_exist(_LMUTIL)
        LMUTIL = [_LMUTIL, 'lmstat', '-c', service_file, '-a']
    else:
        print("TEST MODE INVOKED.")
        LMUTIL = ["cat", "lmstat.txt"]

    LICENSE = os.environ.get('LICENSE') or './service.txt'
    file_must_exist(LICENSE)

    PORT = os.environ.get('PORT') or 5000

    pass

# That's all!

