from sqlalchemy.orm import backref

from database import db


class CustomSerializerMixin:
    pass


class Shareholder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_reg_code = db.Column(db.ForeignKey("company.reg_code"))
    reg_code = db.Column(db.String(11))
    name = db.Column(db.String(100))
    share_amount = db.Column(db.Integer)
    founder = db.Column(db.Boolean(), default=False)
    physical_person = db.Column(db.Boolean(), default=False)

    def json(self):
        return {
            "name": self.name,
            "reg_code": self.reg_code,
            "share_amount": self.share_amount,
            "physical_person": self.physical_person,
            "founder": self.founder,
        }

    def parent_json(self):
        return {"parent_reg_code": self.parent_reg_code}


class Company(db.Model):
    name = db.Column(db.String(100))
    reg_code = db.Column(db.String(7), primary_key=True)
    reg_date = db.Column(db.DateTime)
    shareholders = db.relationship(
        Shareholder, backref=backref("shareholder", single_parent=True, lazy="joined")
    )

    def __init__(self, name, reg_code, reg_date):
        self.name = name
        self.reg_code = reg_code
        self.reg_date = reg_date

    def json(self):
        return {
            "name": self.name,
            "reg_code": self.reg_code,
            "reg_date": self.reg_date.strftime("%Y-%m-%d"),
            "shareholders": [sh.json() for sh in self.shareholders],
        }


class PhysicalPerson(db.Model):
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    reg_code = db.Column(db.String(11), primary_key=True)

    def json(self):
        return {
            "reg_code": self.reg_code,
            "firstName": self.firstName,
            "lastName": self.lastName,
        }
