from __init__ import db, ma
from datetime import datetime
from weekScript import calculate_weeks


class Week(db.Model):
    __tablename__ = "weeks"
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.Date)
    end = db.Column(db.Date)

    def __init__(self, start: datetime, end: datetime):
        self.start = start
        self.end = end

    @staticmethod
    def insert(start, weeks):
        weeks_list = calculate_weeks(start, weeks)
        for interval in weeks_list:
            new_week = Week(interval[0], interval[1])
            db.session.add(new_week)
        db.session.commit()
        return True


class WeekSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Week
