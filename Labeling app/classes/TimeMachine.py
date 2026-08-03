from models import Event, CurrentEvent
import utils
import copy

class Snapshot:
    def __init__(self, events: list[Event], last_event: CurrentEvent):

        """
        The snapshot represents all events and the selected event, in a given moment.

        Args:
            events: List with all of the events in the given moment.
            last_event: The information of the event that is selected in the given moment.
        """
        self.events = copy.deepcopy(events)
        self.last_event = copy.deepcopy(last_event)

class TimeMachine:
    """
    Enables undo and redo commands on the events.

    Attributes:
        time_machine: Stores all of the taken snapshots.
        max_snapshots: The maximum number of snapshots that can be stored.
    """

    time_machine: list[Snapshot] = []
    max_snapshots = 10
    
    def __init__(self, events: list[Event], last_event: CurrentEvent, max_snapshots = 10):
        snapshot = Snapshot(events, last_event)
        self.time_machine.append(snapshot)
        self.snapshot_index = utils.validate_list_index(0, self.time_machine)
        self.max_snapshots = max_snapshots

    def undo(self):
        self.snapshot_index = utils.validate_list_index(self.snapshot_index - 1, self.time_machine)
        snapshot = self.time_machine[self.snapshot_index]
        snapshot_copy = copy.deepcopy(snapshot)
        return snapshot_copy.events, snapshot_copy.last_event

    def redo(self):
        self.snapshot_index = utils.validate_list_index(self.snapshot_index + 1, self.time_machine)
        snapshot = self.time_machine[self.snapshot_index]
        snapshot_copy = copy.deepcopy(snapshot)
        return snapshot_copy.events, snapshot_copy.last_event

    def take_snapshot(self, events: list[Event], current_event: CurrentEvent):
        index = 0 if len(self.time_machine) == 0 else self.snapshot_index + 1
        self.time_machine = self.time_machine[:index]

        self.time_machine[len(self.time_machine) - 1].last_event = current_event

        snapshot = Snapshot(events, current_event)
        self.time_machine.append(snapshot)


        if len(self.time_machine) > self.max_snapshots:
            self.time_machine.pop(0)
        else:
            self.snapshot_index += 1
