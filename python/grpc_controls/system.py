from abc import ABC, abstractmethod, abstractproperty
from typing import Iterable, List, Mapping, Union, Optional, Set, Protocol
import sys
import subprocess
import requests



class Module(Protocol):

    @abstractmethod
    def run(self, *args, **kwargs) -> bool:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @name.setter
    def set_name(self, name) -> None:
        pass
    
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def __enter__(self):
        self.start()

    @abstractmethod
    def __exit__(self, *args):
        self.stop()


class Nested(Protocol):

    @property
    @abstractmethod
    def parent(self) -> Module:
        pass
    
    @parent.setter
    def set_parent(self) -> None:
        pass

    @property
    @abstractmethod
    def children(self) -> 'Nested':
        pass

    @children.setter
    def set_children(self, children):
        pass
    



class PythonModule():
    def run(self, name, *args, **kwargs):
        subprocess.run((sys.executable, '-m', name))

class BaseStationModule():
    def __init__(self, host: str, port: str, cmds: Optional[Set[str]] = None, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.host, self.port = host, port
        self.cmds = cmds if not None else set()

    def run(self, cmd, params):
        if cmd not in self.cmds:
            return
        requests.get(f'{self.host}:{self.port}/{cmd}', params)

class System():

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
