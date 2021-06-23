# flake8: noqa

import stactools.core

stactools.core.use_fsspec()


def register_plugin(registry):
    # Register subcommands

    from stactools.aster import commands

    registry.register_subcommand(commands.create_aster_command)


__version__ = '0.2.1a1'
"""Library version"""
