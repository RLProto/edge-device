from app.backend.models.StatusType import StatusType


class StatusHandler:
    def __init__(self):
        self.continuous_status = None
        self.last_status = None

    def set_status(self, data):
        self.continuous_status = data["status"] == StatusType.START.value

    def set_last_status(self):
        self.last_status = self.continuous_status

    def check_process_running_status(self):
        if self.continuous_status == True:
            if self.last_status == True:
                return True
        return False

    def able_to_infere(self):
        return not self.continuous_status == True
