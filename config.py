import os

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

    TEST_MODE = False
    TEST_FILE = 'lmstat.txt'

    LMHOME  = os.environ.get('LMHOME') or '.'
    LICENSE = os.environ.get('LICENSE') or 'service.txt'
    _LMUTIL = os.environ.get('LMUTIL')
    if _LMUTIL:
        # Holy cow but Windows was super fussy about this section.
        # It would not accept running the actual file with .exe on it.
        # It was impossible to pass spaces in args. Gag me, let me have Linux.
        os.chdir(LMHOME)
        file_must_exist(_LMUTIL)
        file_must_exist(LICENSE)
        LMUTIL = [_LMUTIL, 'lmstat', '-c', LICENSE, '-a']
    else:
        print("TEST MODE INVOKED.")
        TEST_MODE = True

    if not TEST_MODE:
        file_must_exist(LICENSE)

    pass

# That's all!

