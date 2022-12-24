from abc import ABC, abstractmethod
from typing import Iterable, List, Optional, Set, Protocol
import sys
import subprocess
from threading import Thread
import requests
import time


class Module(Protocol):

    """
    Specifies the following methods. See the function's docs to see more info.
    
    ATTRIBUTES
    ----------
    name
        - The name property.

    METHODS
    -------
    run(*args, **kwargs)
        - This method will initiate the execution of the appropriate model upon execution,
          within the appropriate context.
    
    start()
        - Start the module. Usually automatically called upon context set up.
    
    stop()
        - Stop the module. Usually automatically called upon context exit.
    
    __enter__()
        - Defined to explictily have protocols implement the context functions.
          Called when entering the Module context.
    
    __exit__()
        - Defined to explictily have protocols implement the context functions.
          Called when exiting the Module context.

    """

    @abstractmethod
    def run(self, *args, **kwargs) -> bool:
        """
        Called to execute a command.

        *args
            - The positional arguments to pass the Module as it initiates execution.
        
        **kwargs
            - The key word arguments to pass to the command.
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """
        The name property of the Module.
        """
        pass

    @name.setter
    def set_name(self, name_: str) -> None:
        """
        Set the name of the module to the name_ parameter.

        name_
            - The new name of the module.
        """
        pass
    # TODO: Finish documenting the rest.
    @abstractmethod
    def start(self) -> None:
        """
        Starts the module.
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """
        Stops the module.
        """
        pass

    def __enter__(self) -> 'Module':
        """
        Enter
        """
        self.start()

    def __exit__(self, *args) -> None:
        """
        Exit
        """
        self.stop()


class Nested(Protocol):
    """
    A type that allows for traversal of parent and children relationships (a tree).
    """

    _parent: 'Nested'

    @property
    @abstractmethod
    def parent(self) -> 'Nested':
        """
        The parent of the current object.
        """
        return self._parent
    
    @parent.setter
    def adopt(self, p: 'Nested') -> None:
        """
        Reassigns the parent to p. This also removes the child from the old parent.

        p
            - The new parent.
        """
        old_parent = self._parent

        self._parent = p
        old_parent.children.remove(self)
        p.children.append(self)

    @property
    @abstractmethod
    def children(self) -> List['Nested']:
        """
        Returns the current children from this Nested object.
        """
        pass

    @children.setter
    def set_children(self, children: List['Nested']) -> None:
        """
        Sets the children for this node to `children`. 
        """
        pass
    
class PythonModule(Module):
    class Launcher(Thread):
        _result = None
        """
        Used to asynchronously launch the python module.
        """
        module: 'PythonModule'
        def __init__(self, module: 'PythonModule'):
            self.module = module

        def run(self):
            self.module.run()
        
        @property
        def result(self):
            try:
                return self._result
            finally:
                self._result = None
        
        @result.setter
        def result(self, value):
            self._result = value

    def __init__(self, name, *args, exec: str = sys.executable, **kwargs):
        """
        PARAMETERS
        ----------
        name
            The name of the python module to be started.
        args
            These args are automatically passed to the python module.
        exec
            (kwarg) The python executable. Defaults to current executable
        kwargs
            These keywords args are automatically passed to the python module.
        """
        self.name, self.exec, self.args, self.kwargs = name, exec, args, kwargs
        self.launcher = PythonModule.Launcher(self)

    def run(self, async_: bool = True) -> bool:
        '''
        Runs the module. (Please override pydoc)
        
        RETURNS
        -------
        bool -
            Whether the process successfully returned or not
        '''
        if async_:
            self.launcher.start()
        return 

    @property
    def name(self) -> str:
        """
        The name of the python module to be started.
        """
        return self._name

    @name.setter
    def set_name(self, name: str) -> None:
        """
        Name setter

        PARAMETERS
        ----------
        name
            The full, dot-separated module name. For example, if we had a Module named
            `FacialRecModule` located in the my.facerec package, the full name would be my.facerec.FacialRecModule.
        """
        self._name = name

    def start(self) -> None:
        return None
    
    def stop(self) -> None:
        return None

    def __enter__(self) -> Module:
        return self

    def __exit__(self) -> None:
        return None


class ExternServerModule(Module):
    def __init__(self, host: str, port: str, cmds: Optional[Set[str]] = None, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.host, self.port = host, port
        self.cmds = cmds if not None else set()

    def run(self, cmd, params):
        if cmd not in self.cmds:
            return
        requests.get(f'{self.host}:{self.port}/{cmd}', params)

    @property
    def name(self):
        pass

    @name.setter
    def set_name(self, name):
        self._name = name

    def start(self):
        pass
    
    def stop(self):
        pass
    
    def _check_connection(self, notify=True):
        ping_start = time.time_ns()
        params = {
            'ping_start': ping_start,
            'notify': notify
        }
        r = requests.get(f'{self.host}:{self.port}/test_connection', params=params)
        r.raise_for_status()
        # latency
        return time.time_ns() - ping_start

    def __enter__(self):
        self._check_connection()

    def __exit__(self):
        pass

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


    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass



