import fire
import json
from abc import ABCMeta, abstractmethod
import subprocess
from textwrap import dedent
"""
Proxy Manager

cmd:
xim set
xim now

xim shell set
xim shell unset
xim shell list

xim proxy add
xim proxy delete
xim proxy list

memo: 
https://username:passward@url:port

Xim:
    =Console:
        list()
    =ConfigJSONFile
    <== Load ==
    =Shells:
        =List<Shell>:
            =path
            run()
        set()
        unset()
        list()
    
    =ProxiesJSONFile
    == Create ==>
    =Proxies:
        =List<Proxy>:
            =name, username, password, domain, port
        add()
        delete()
        list()
        now()
        
"""


class Console:
    def __init__(self):
        pass

    def list(self, param):
        max_l = [0] * len(param[0])
        for i, ii in enumerate(param):
            for j, jj in enumerate(ii):
                max_l[j] = max(max_l[j], len(str(jj)))
        for i, ii in enumerate(param):
            for j, jj in enumerate(ii):
                print(jj, end=" " * (max_l[j] - len(str(jj)) + 1) + "| ")
            print("")


class DataFile(metaclass=ABCMeta):
    def __init__(self, file_path):
        """

        :param file_path: string
        """
        self.file_path = file_path

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def dump(self, data):
        pass


class ProxiesJSONFile(DataFile):
    def __init__(self, file_path):
        """

        :param file_path: string
        """
        super().__init__(file_path)

    def load(self):
        with open(self.file_path, "r") as f:
            return Proxies(json.loads(f.read()))

    def dump(self, proxies):
        with open(self.file_path, "w") as f:
            return f.write(json.dumps(proxies.proxies))


class ConfigJSONFile(DataFile):
    def __init__(self, file_path):
        """

        :param file_path: string
        """
        super().__init__(file_path)

    def load(self):
        with open(self.file_path, "r") as f:
            return Config(json.loads(f.read()))

    def dump(self, config):
        with open(self.file_path, "w") as f:
            return f.write(json.dumps(config.config))


class Config:
    def __init__(self, config_dict):
        self.config = config_dict

    def get_shells(self):
        return self.config["shells"]

    def set_shells(self, shells):
        self.config["shells"] = shells

    def get_now(self):
        return self.config["already_set"]

    def set_now(self, now):
        self.config["already_set"] = now


class Proxy:
    def __init__(self, name, http, https):
        """
        """
        self.name = name
        self.http = http
        self.https = https

    def dict(self):
        return {"http": self.http, "https": self.https}

    def values(self):
        return [self.http, self.https]


class Proxies:
    def __init__(self, proxy_dict):
        self.proxies = proxy_dict

    def create(self, proxy):
        self.proxies[proxy.name] = proxy.dict()

    def delete(self, name):
        del self.proxies[name]

    def read(self, name):
        return Proxy(name, self.proxies[name]["http"], self.proxies[name]["https"])

    def list(self):
        keys = list(self.proxies.keys())
        values = list(self.proxies.values())
        return [[keys[i], *values[i].values()] for i in range(len(keys))]


class XimProxy:
    def __init__(self, proxies):
        self.proxies = proxies

    def add(self, name, http, https):
        """

        :param name: string
        :param http: string
        :param https: string
        :return: void
        """
        self.proxies.create(Proxy(name, http, https))

    def delete(self, name):
        """

        :param name: string
        :return: void
        """
        self.proxies.delete(name)

    def list(self):
        Console().list(self.proxies.list())

    def help(self):
        print(dedent("""
        xim proxy add <proxy name> <http proxy> <https proxy>
            add proxy setting.
        xim proxy delete <proxy name>
            delete proxy setting.
        xim proxy list
            show set proxy list.
        xim proxy help
            show help.
        """))


class Shell:
    def __init__(self, name):
        """

        :param name: string
        """
        self.name = name


class Shells:
    def __init__(self, shell_dict, shells_dir_path):
        """

        :param shell_dict: dict
        """
        self.shells = shell_dict
        self.shells_dir_path = shells_dir_path

    def read(self, name):
        return self.shells[name]

    def set(self, name):
        """

        :param name: string
        :return: void
        """
        if name not in self.shells.keys():
            raise KeyError
        self.shells[name] = True

    def unset(self, name):
        """

        :param name: string
        :return: void
        """
        if name not in self.shells.keys():
            raise KeyError
        self.shells[name] = False

    def list(self):
        """

        :return: list
        """
        keys = list(self.shells.keys())
        values = list(self.shells.values())
        return [[keys[i], values[i]] for i in range(len(keys))]

    def run(self, name, arg):
        subprocess.run([self.shells_dir_path + name + ".cmd", *arg.values()])

    def run_all(self, arg):
        for shell in self.shells:
            if self.shells[shell]:
                self.run(shell, arg)


class XimShell:
    def __init__(self, shells):
        self.shells = shells

    def set(self, *shell_names):
        """

        :param shell_names: Tuple<string>
        :return: void
        """
        if type(shell_names[0]) == tuple:
            for shell_name in shell_names[0]:
                print(shell_name)
                self.shells.set(shell_name)
        else:
            self.shells.set(shell_names[0])

    def unset(self, *shell_names):
        """

        :param shell_name: string
        :return: void
        """
        if type(shell_names[0]) == tuple:
            for shell_name in shell_names[0]:
                print(shell_name)
                self.shells.unset(shell_name)
        else:
            self.shells.unset(shell_names[0])

    def list(self):
        Console().list(self.shells.list())

    def help(self):
        print(dedent("""
        xim shell set <shell(s)>
            set shell.
            ex.)
                xim shell set npm
                xim shell set pip,npm,git
        xim shell unset <shell(s)>
            unset shell. (how to use is upper)
        xim shell list
            show shells status.
        xim shell help
            show help
        ! caution !
        git shell is set in --global.
        """))


class Xim:
    def __init__(self, proxies_path=r"./proxies.json", config_path=r"./xim.config.json",
                 shells_dir_path=".\\shells\\"):
        self.proxies_file = ProxiesJSONFile(proxies_path)
        self.config_file = ConfigJSONFile(config_path)
        self.proxies = self.proxies_file.load()
        self.config = self.config_file.load()
        self.shells = Shells(self.config.get_shells(), shells_dir_path)
        self.now = self.config.get_now()
        # Commands
        self.shell = XimShell(self.shells)
        self.proxy = XimProxy(self.proxies)

    def __del__(self):
        self.proxies_file.dump(self.proxy.proxies)
        self.config.set_shells(self.shells.shells)
        self.config.set_now(self.now)
        self.config_file.dump(self.config)

    def set(self, proxy_name):
        """

        :param proxy_name: string
        :return: void
        """
        self.shells.run_all(self.proxies.read(proxy_name))
        self.now = proxy_name

    def now(self):
        print(self.now)

    def help(self):
        print(dedent("""
        xim set <proxy name>
            run set shell.
        xim now
            show applied proxy.
        xim help
            show help.
        xim shell <command>
            => xim shell help
        xim proxy <command>
            => xim proxy help
        """))


if __name__ == "__main__":
    fire.Fire(Xim)
