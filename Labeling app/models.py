from globals import vidDetails

class Event:
    def __init__(self, start_time = 0, end_time = 0, label = ""):
        """
        Args:
            start_time: The moment the event started. 
            end_time: The moment the event ended.
            label: The label of the event.
        """
        self.recording_id = vidDetails.recording_id
        self.start_time = start_time
        self.end_time = end_time
        self.label = label

class CurrentEvent(Event):
    """Represents the event that is selected at the moment."""
    def __init__(self, index: int, start_time = 0, end_time = 0, label = "", event: Event = None):
        """
        Represents the event that is selected at the moment.
        
        Args:
            index: The index of the event in the "events" array.
            start_time: The moment the event started. 
            end_time: The moment the event ended.
            label: The label of the event.
            event: Event that already exists, and have to become the current one. 

        If event is set, all other arguments will not be used except for the index 
        """

        if event != None:
            super().__init__(event.start_time, event.end_time, event.label)
        else:
            super().__init__(start_time, end_time, label)
        
        self.index = index