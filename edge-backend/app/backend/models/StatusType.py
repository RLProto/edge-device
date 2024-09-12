from enum import Enum


class StatusType(Enum):
    """
    Enumerates types of status supported in the system, providing a way to handle different statys types consistently.
    """

    START = "start"
    STOP = "stop"
