"""The component base the ComfoConnect PRO register map builds on."""

from __future__ import annotations

from modbus_connection.model import Component, UpdateReport

__all__ = ["ComfoConnectComponent", "UpdateReport", "address"]


def address(number: int) -> int:
    """The protocol address of an entry the manual lists at ``number``.

    The manual counts from 1 in every table, so its input register 0x0001 is
    address 0.
    """
    return number - 1


class ComfoConnectComponent(Component):
    """A sub-system of the ComfoConnect PRO register map."""
