from prompts import *






class Memory:
    def __init__(self, chats):
        self.chats = chats

    def add_system_message(self, message: str) -> list[dict]:
        new_message = {
            "role": "system",
            "content": message
        }
        self.chats.append(new_message)
        return self.chats 
    
    def add_patient_message(self, message: str) -> list[dict]:
        message_prefix=f"<PATIENT> {message}"
        new_message = {
            "role": "user",
            "content": message_prefix
        }
        self.chats.append(new_message)
        return self.chats

    def add_doctor_message(self, message: str) -> list[dict]:
        message_prefix_suffix=f'''<DOCTOR> {message} Make sure you only ask one question at one time . 
        Otherwise the patient will die answering.''' 
        new_message = {
            "role": "user",
            "content": message_prefix_suffix
        }
        self.chats.append(new_message)
        return self.chats
    
    def add_doctor_prescription_message(self, message: str) -> list[dict]:
        message_prefix_suffix=f'''<DOCTOR> {message} This is the prescription to be 
        administered by the patient . Motivate the patient to take the prescription. ''' 
        new_message = {
            "role": "user",
            "content": message_prefix_suffix
        }
        self.chats.append(new_message)
        return self.chats
    
    def add_doctor_suggestion_message(self, message: str) -> list[dict]:
        message_prefix_suffix=f'''<DOCTOR> {message} This are the suggestions to be given to
        patient . Motivate the patient to follow the suggestions. ''' 
        new_message = {
            "role": "user",
            "content": message_prefix_suffix
        }
        self.chats.append(new_message)
        return self.chats

    def add_assistant_message(self, message: str) -> list[dict]:
        new_message = {
            "role": "assistant",
            "content": message
        }
        self.chats.append(new_message)
        return self.chats
    
    
    def print_chat(self):
        print(self.chats)

    def get_chats(self):
        return self.chats
    
    def reset_memory(self):
        self.chats = []




