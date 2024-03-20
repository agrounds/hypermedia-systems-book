import json


class Contact:
    contacts = {}

    def __init__(self, id_=None, first=None, last=None, phone=None, email=None):
        self.id = id_
        self.first = first
        self.last = last
        self.phone = phone
        self.email = email
        self.errors = {}

    def __str__(self):
        return json.dumps({
            'id': self.id,
            'first': self.first,
            'last': self.last,
            'phone': self.phone,
            'email': self.email,
        }, ensure_ascii=False)

    def update(self, first, last, phone, email):
        self.first = first
        self.last = last
        self.phone = phone
        self.email = email

    def save(self):
        if self.id is None:
            if len(Contact.contacts) > 0:
                self.id = max(self.contacts.keys()) + 1
            else:
                self.id = 1
        Contact.contacts[self.id] = self
        Contact.save_db()
        return True

    @classmethod
    def load_db(cls):
        try:
            new_contacts = {}
            with open('../data/contacts.jsonl', 'r') as f:
                for line in f:
                    parsed = json.loads(line)
                    new_contacts[parsed['id']] = Contact(
                        id_=parsed['id'],
                        first=parsed['first'],
                        last=parsed['last'],
                        phone=parsed['phone'],
                        email=parsed['email'],
                    )
            cls.contacts = new_contacts
        except FileNotFoundError:
            cls.save_db()

    @classmethod
    def save_db(cls):
        with open('../data/contacts.jsonl', 'w') as f:
            for contact in cls.contacts.values():
                f.write(f'{contact}\n')

    @classmethod
    def search(cls, text):
        result = []
        for c in cls.contacts.values():
            match_first = c.first is not None and text in c.first
            match_last = c.last is not None and text in c.last
            match_email = c.email is not None and text in c.email
            match_phone = c.phone is not None and text in c.phone
            if match_first or match_last or match_email or match_phone:
                result.append(c)
        return result

    @classmethod
    def all(cls):
        return cls.contacts.values()

    @classmethod
    def find(cls, id_):
        return cls.contacts.get(id_)

    @classmethod
    def delete(cls, id_):
        del cls.contacts[id_]
        cls.save_db()
