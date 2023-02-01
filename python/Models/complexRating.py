from __init__ import db, ma
from datetime import datetime, timedelta
from sqlalchemy import ForeignKey
from Models.week import Week
from Models.course import Course


class ComplexRating(db.Model):
    __tablename__ = "complex_ratings"
    id = db.Column(db.Integer, primary_key=True)
    clarity_rating = db.Column(db.Integer)
    interactivity_rating = db.Column(db.Integer)
    relevance_rating = db.Column(db.Integer)
    course_id = db.Column(db.Integer, ForeignKey(
        "courses.id", ondelete="CASCADE"), nullable=False)
    date = db.Column(db.DateTime)

    def __init__(self, clarity_rating: int, interactivity_rating: int, relevance_rating: int, course_id: int, date: datetime):
        self.clarity_rating = clarity_rating
        self.interactivity_rating = interactivity_rating
        self.relevance_rating = relevance_rating
        self.course_id = course_id
        self.date = date

    @staticmethod
    def create(clarity_rating: int, interactivity_rating: int, relevance_rating: int, room: str, date: datetime):
        course_id = ComplexRating.get_course_id(date, room)
        if course_id:
            if ComplexRating.insert(clarity_rating, interactivity_rating, relevance_rating, course_id, date):
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def insert(clarity_rating: int, interactivity_rating: int, relevance_rating: int, course_id: int, date: datetime):
        try:
            new_rating = ComplexRating(
                clarity_rating, interactivity_rating, relevance_rating, course_id, date)
            db.session.add(new_rating)
            db.session.commit()
            return True
        except:
            return False

    @staticmethod
    def get_course_id(date: datetime, room: str):
        week_type = 0
        week = Week.query.filter(Week.start < date).filter(
            Week.end > date).first()
        if week.id % 2 == 0:
            week_type = 2
        else:
            week_type = 1
        weekday = date.weekday()+1
        time = date.time()
        course = Course.query.filter((Course.week_type == week_type) | (Course.week_type == 0)).filter(
            Course.day == weekday).filter(Course.start < time).filter(Course.end > time).filter(Course.room == room).first()
        if course:
            return course.id

    @staticmethod
    def mean_per_day(start: datetime, end: datetime, course_id: int):
        delta = timedelta(days=1)
        data = []
        while start <= end:
            clarity = 0
            interactivity = 0
            relevance = 0
            mean_clarity = 0
            mean_interactivity = 0
            mean_relevance = 0
            ratings_list = ComplexRating.retrieve_ratings(
                start, start+delta, course_id)
            for rating in ratings_list:
                clarity += rating['clarity_rating']
                interactivity += rating['interactivity_rating']
                relevance += rating['relevance_rating']
                mean_clarity = clarity/len(ratings_list)
                mean_interactivity = interactivity/len(ratings_list)
                mean_relevance = relevance/len(ratings_list)
            if mean_clarity != 0:
                data.append({"mean_clarity": round(mean_clarity, 2), "mean_interactivity": round(mean_interactivity, 2),
                            "mean_relevance": round(mean_relevance, 2), "date": start})
            start += delta
        return data

    @staticmethod
    def total_mean(course_id: int):
        ratings_list = ComplexRating.retrieve_ratings(
            "01/01/2022", datetime.today(), course_id)
        clarity = 0
        interactivity = 0
        relevance = 0
        for rating in ratings_list:
            clarity += rating['clarity_rating']
            interactivity += rating['interactivity_rating']
            relevance += rating['relevance_rating']
        return {"mean_clarity": round(clarity/len(ratings_list), 2), "mean_interactivity": round(interactivity/len(ratings_list), 2),
                "mean_relevance": round(relevance/len(ratings_list), 2)}

    @staticmethod
    def retrieve_ratings(start: datetime, end: datetime, course_id: int):
        ratings = ComplexRating.query.filter(ComplexRating.course_id == course_id).filter(
            ComplexRating.date.between(start, end))
        ratings_schema = ComplexRatingSchema(many=True)
        ratings_list = ratings_schema.dump(ratings)
        return ratings_list


class ComplexRatingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ComplexRating
