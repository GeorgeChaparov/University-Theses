from modules import Event, CurrentEvent
import utils

import pandas as pd
from PyQt6.QtCore import pyqtSignal, QObject

class EventHandler(QObject):
    """
    Handles all CRUD actions for events

    Attributes:
        current_event: The event that is currently selected.
        current_event_changed: Event, fired when the current event have changed.
        events_change_requested: Event, fired when the array "events" have changed. 
    """


    current_event_changed = pyqtSignal(str)
    events_change_requested = pyqtSignal(int)

    current_event = CurrentEvent(0)

    def __init__(self, events: list[Event]):
        super().__init__()
        self.__events = events


    @property
    def events(self):
        return self.__events
    
    @events.setter
    def events(self, value):
        self.__export_events()
        self.__events = value


    def update_current_event_label(self, new_label: str):
        
        old_event = self.events[self.current_event.index]
        new_event = Event(old_event.start_time, old_event.end_time, new_label)
        self.events[self.current_event.index] = new_event
        self.set_current_event(self.current_event.index)

        self.__export_events()
        self.events_change_requested.emit(self.current_event.start_time)

    def delete_current_event(self):

        self.__delete_event(self.current_event.index)

    def add_event(self, label: str, end_time: int, delay: int):
        """
        Adds new event
        
        Args: 
            label: The label of the new event.
            end_time: The end time of the event.
            delay: The delay used to display the gaze.
        """

        # First event ever
        if len(self.events) == 0:
            start = 0
        else:
            start = self.current_event.end_time

        end = end_time

        if start == end_time:
            raise ValueError("The start time cannot be the same as the end time.")

        # Save event
        event = Event(start, end, label)
        self.events.append(event)

        end = max(0, end - delay)

        if start <= end:
            end += 1

        self.__export_events()

        # Update state
        self.set_current_event(self.current_event.index + 1)
        self.events_change_requested.emit(self.current_event.end_time)

    def split_event(self, time: int):
        """
        Splits an event to two events. 
        The first event have the start time of the current event and the end time of the "time" argument. 
        The second event have the start time of the "time" argument and the end time of the current event.

        Args:
            time: The time at which the event will be split.
        """

        if  self.current_event.start_time > time or self.current_event.end_time < time:
            raise ValueError("The time have to be between the start and the end time of the current event.")
        
        new_event = Event(self.current_event.start_time, time, self.current_event.label)

        self.events[self.current_event.index].start_time = time
        self.events.insert(self.current_event.index, new_event)

        self.set_current_event(self.current_event.index + 1)
        self.events_change_requested.emit(self.current_event.start_time)

    def change_start_time(self, time: int):
        if self.current_event.end_time < time:
            raise ValueError("The time have to be smaller then the end time of the current event.")

        # Change the start time of the current event
        self.events[self.current_event.index].start_time = time

        # Check if there is another event before that one.
        # Check if the new start time is smaller then the start time of the last event.
        # And if so, delete the last event. Do this for all events before the current one.
        index_to_check = self.current_event.index
        while True:
            if index_to_check > 0:
                index_to_check = self.current_event.index - 1

                prev_event = self.events[index_to_check]
                if prev_event.start_time < time:
                    prev_event.end_time = time

                    break
                else:
                    self.__delete_event(index_to_check, self.current_event.index)
                    index_to_check -= 1
            else:
                break

        self.events_change_requested.emit(self.current_event.start_time)


    def change_end_time(self, time: int):
        if self.current_event.start_time > time:
            raise ValueError("The time have to be smaller then the start time of the current event.")

        # Change the end time of the current event
        self.events[self.current_event.index].end_time = time

        # Check if there is another event after that one.
        # Check if the new end time is bigger then the end time of the next event.
        # And if so, delete the next event. Do this for all events after the current one.
        index_to_check = self.current_event.index
        while True:
            if index_to_check < len(self.events) - 1:
                index_to_check = self.current_event.index + 1

                next_event = self.events[index_to_check]
                if next_event.end_time > time:
                    next_event.start_time = time

                    break
                else:
                    self.__delete_event(index_to_check, self.current_event.index)
                    index_to_check += 1
            else:
                break

        self.events_change_requested.emit(self.current_event.start_time)
    
    def set_current_event(self, index: int):
        """
        Sets the current event to the event with the given index.
        
        Args:
            index: The index of the event that is to be set as the current one.
        """

    
        try:
            idx = utils.validate_list_index(index, self.events)
        except IndexError as e:
            print(e)
            return
        
        event = self.events[idx]

        self.current_event = CurrentEvent(idx, event = event)

        self.current_event_changed.emit(self.current_event.label)
    


    def __delete_event(self, index: int, new_current_event_idx = -1):
        """
        Deletes the event with the given index.

        Args:
            index: The index of the event that is to be deleted.
            new_current_event_idx: The index of the event that is to become the current event. If not set, the current event becomes the last one.
        """

        try:
            idx = utils.validate_list_index(index, self.events)
        except IndexError as e:
            print(e)
            return
        
        event_to_del = self.events[idx]

        self.events.remove(event_to_del)

        self.__export_events()
        if new_current_event_idx == -1:
            self.set_current_event(self.current_event.index - 1)
        else:
            try:
                idx = utils.validate_list_index(new_current_event_idx, self.events)
            except IndexError as e:
                print(e)
                return
            
            self.set_current_event(new_current_event_idx)

        self.events_change_requested.emit(self.current_event.end_time)

    def __export_events(self):
        df = pd.DataFrame([
            {
                "recording id": event.recording_id,
                "start timestamp [ms]": event.start_time,
                "end timestamp [ms]": event.end_time,
                "label": event.label,
            }
            for event in self.events
        ])

        utils.save_df_to_csv(df, True)