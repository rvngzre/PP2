class Message:
    def send(self):
        return "Send"

class Email(Message):
    def send(self):
        return "Email"

class Sms(Message):
    def send(self):
        return "SMS"

class Push(Message):
    def send(self):
        return "Push"

print(Email().send())
print(Sms().send())
print(Push().send())
print(Message().send())
