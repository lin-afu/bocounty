import os
from Enums.FlaskConfigEnum import FlaskConfigEnum as ConfigEnum
import pickle

CONFIGURENAME = './bocounty.config'


class Configure:
    def __init__(self) -> None:
        self.full_file_path = os.path.join(os.getcwd(), CONFIGURENAME)
        if os.path.exists(self.full_file_path):
            with open(self.full_file_path, "rb") as file:
                self.configure = pickle.loads(file.read())
        else:
            # self.configure = {
            #     'JWT_secret': 'DefaultSecret',
            #     'SSL': {
            #         "Enable": "false"
            #     },
            #     'SQL': {
            #         'Host': '127.0.0.1',
            #         'User': 'root',
            #         'Password': 'Shaker8787',
            #         'Database': 'bocounty'
            #     },
            #     'Encrypt': {
            #         'PublicKeyPath': './public.pem',
            #         'PrivateKeyPath': './private.pem'
            #     },
            #     'UploadFolder': "./static/picture/",
            # }
            self.configure = {
                ConfigEnum.JWT_secret: 'DefaultSecret',
                ConfigEnum.SSL: {
                    "Enable": "false"
                },
                ConfigEnum.SQL: {
                    'Host': '127.0.0.1',
                    'User': 'root',
                    'Password': '12345678',
                    'Database': 'bocounty'
                },
                ConfigEnum.Encrypt: {
                    'PublicKeyPath': './public.pem',
                    'PrivateKeyPath': './private.pem'
                },
                ConfigEnum.UploadFolder: "./static/picture/",
            }
            self.commit_change()
    def commit_change(self) -> None:
        with open(self.full_file_path, "wb") as file:
            file.write(pickle.dumps(self.configure))

    def __str__(self) -> str:
        return str(self.configure)

    def __setitem__(self, key, item):
        self.configure[key] = item

    def __getitem__(self, key):
        return self.configure[key]

    def __repr__(self):
        return repr(self.configure)

    def __len__(self):
        return len(self.configure)

    def __delitem__(self, key):
        del self.configure[key]

    def clear(self):
        return self.configure.clear()

    def copy(self):
        return self.configure.copy()

    def has_key(self, k):
        return k in self.configure

    def update(self, *args, **kwargs):
        return self.configure.update(*args, **kwargs)

    def keys(self):
        return self.configure.keys()

    def values(self):
        return self.configure.values()

    def items(self):
        return self.configure.items()

    def pop(self, *args):
        return self.configure.pop(*args)

    def __cmp__(self, dict_):
        return self.__cmp__(self.configure, dict_)

    def __contains__(self, item):
        return item in self.configure

    def __iter__(self):
        return iter(self.configure)

    def __unicode__(self):
        return unicode(repr(self.configure))
