from abc import ABC, abstractmethod, abstractproperty
from typing import Iterable, List, Mapping, Union, Optional, Set
import sys
import subprocess
import requests



class Module(ABC):
    @abstractmethod
    def run(self, *args, **kwargs):
        pass

class PythonModule(Module):
    def run(self, name, *args, **kwargs):
        subprocess.run((sys.executable, '-m', name))

class BaseStationModule(Module):
    def __init__(self, host, port, cmds: Optional[Set[str]] = None, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.host, self.port = host, port
        self.cmds = cmds if not None else set()

    def run(self, cmd, params):
        if cmd not in self.cmds:
            return
        requests.get(f'{self.host}:{self.port}/{cmd}', params)

class System(ABC):

    _modules: List[Module] = []

    def __init__(self, name, modules, *args, **kwargs):
        self._name = name
        self._modules.extend(modules)


    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name_):
        self._name = name_
    
    @property
    def modules(self):
        return self._modules

    @modules.setter
    def modules(self, modules_ : Iterable[Module]):
        self._modules.clear()
        self._modules.extend(modules_)
