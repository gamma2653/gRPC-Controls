DEFAULT_MODULES = None
DEFAULT_CHAOS = 10.0

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from argparse import ArgumentParser

def _create_if_not_exist(coll):
    return [] if coll is None else coll

def bind_args(parser: ArgumentParser):
    parser.add_argument('-m', '--modules', nargs='+', default=_create_if_not_exist(DEFAULT_MODULES))
    parser.add_argument('-c', '--chaos', action='store', type=float, default=DEFAULT_CHAOS)

if TYPE_CHECKING:
    del ArgumentParser