class Lesson:
    def __init__(self, subject, teacher, group, audience, pair, day):
        self.subject = subject
        self.teacher = teacher
        self.group = group
        self.audience = audience
        self.pair = pair
        self.day = day

    def print(self):
        print(f"day:{self.day}")
        print(f"pair:{self.pair}")
        print(f"teacher:{self.teacher.name}")
        print(f"group:{self.group.name}")
        print(f"audience:{self.audience.name}")
        print(f"subject:{self.subject.name}")

class Teacher:
    def __init__(self, name, hours, subjects):
        self.name = name
        self.hours = hours
        self.subjects = subjects

class Subject:
    def __init__(self, name):
        self.name = name

class Group:
    def __init__(self, name, subjects_hours):
        self.name = name
        self.subjects_hours = subjects_hours

class Audience:
    def __init__(self, name):
        self.name = name