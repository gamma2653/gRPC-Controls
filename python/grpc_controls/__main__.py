import argparse

from grpc_controls import config

parser = argparse.ArgumentParser()

config.bind_args(parser)

args, unknown_args = parser.parse_known_args()


