import os

basedir = os.path.abspath(os.path.dirname(__file__))

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

    SECRET_KEY = os.environ.get("SECRET_KEY", "ineedakey")

    TEST_MODE = False
    TEST_FILE = os.path.join(basedir, 'lmstat.txt')

    LMHOME  = os.environ.get('LMHOME', '.')
    LICENSE = os.environ.get('LICENSE', 'service.txt')
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
        # TEST MODE INVOKED
        LMUTIL = TEST_FILE
        TEST_MODE = True

    if not TEST_MODE:
        file_must_exist(LICENSE)

    pass

    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    DEBUG = True

class TestConfig(Config):
    TESTING = True
    DEBUG = True

class ProdConfig(Config):
    DEBUG = False


config = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProdConfig,
    'default': DevConfig
}

# That's all!

