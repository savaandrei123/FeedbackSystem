from flask import Blueprint, request, jsonify, session, make_response
from datetime import datetime, timedelta
from Models.basicRating import BasicRating
from Models.week import Week
from Models.course import Course
from Models.professor import Professor
from Models.faculty import Faculty
from Models.programme import Programme
from Models.complexRating import ComplexRating
from Models.programmeCourses import ProgrammeCourses
import json

basic_rating_bp = Blueprint('basic_ratings', __name__)
complex_rating_bp = Blueprint('complex_ratings', __name__)
course_bp = Blueprint('courses', __name__)
professor_bp = Blueprint('professors', __name__)
week_bp = Blueprint('weeks', __name__)
faculty_bp = Blueprint('faculties', __name__)
programme_bp = Blueprint("programmes", __name__)
prog_courses_bp = Blueprint("programmes_courses", __name__)

# PROFESSOR ENDPOINTS


@professor_bp.route("/professors", methods=["GET"])
def get_professors():
    response = Professor.get_professors()
    return {"response": response}


@professor_bp.route("/createprofessor", methods=["POST"])
def create_professor():
    name = request.args.get('name')
    if Professor.create(name):
        return {"response": "professor created"}, 200
    else:
        return {"response": "error"}, 500


@professor_bp.route("/updateprofessor", methods=["PUT"])
def update_professor():
    id = int(request.args.get('id'))
    name = request.args.get('name')
    if Professor.update(id, name):
        return {"response": "professor updated"}, 200
    else:
        return {"response": "error"}, 500


@professor_bp.route("/deleteprofessor", methods=["DELETE"])
def delete_professor():
    id = int(request.args.get("id"))
    if Professor.delete(id):
        return {"response": "professor deleted"}, 200
    else:
        return {"response": "error"}, 500


@professor_bp.route("/professorcourses", methods=["GET"])
def get_professor_courses():
    id = int(request.args.get("id"))
    result = Professor.get_courses(id)
    return {"response": result}, 200

# FACULTY ENDPOINTS


@faculty_bp.route("/faculties", methods=["GET"])
def get_faculties():
    result = Faculty.get_faculties()
    return {"response": result}


@faculty_bp.route("/createfaculty", methods=["POST"])
def create_faculty():
    name = request.args.get("name")
    years = int(request.args.get("years"))
    if Faculty.create(name, years):
        return {"response": "faculty created"}, 200
    else:
        return {"response": "error"}, 500


@faculty_bp.route("/updatefaculty", methods=["PUT"])
def update_faculty():
    id = int(request.args.get("id"))
    name = request.args.get("name")
    years = int(request.args.get("years"))
    if Faculty.update(id, name, years):
        return {"response": "faculty updated"}, 200
    else:
        return {"response": "error"}, 500


@faculty_bp.route("/deletefaculty", methods=["DELETE"])
def delete_faculty():
    id = int(request.args.get("id"))
    if Faculty.delete(id):
        return {"response": "faculty deleted"}, 200
    else:
        return {"response": "error"}, 500


@faculty_bp.route("/facultyprogrammes", methods=["GET"])
def get_faculty_programmes():
    id = int(request.args.get("id"))
    result = Faculty.get_programmes(id)
    return {"response": result}, 200


@faculty_bp.route("/facultycourses", methods=["GET"])
def get_faculty_courses():
    id = int(request.args.get("id"))
    result = Faculty.get_courses(id)
    return {"response": result}, 200


@faculty_bp.route("/facultyyears", methods=["GET"])
def get_faculty_years():
    id = int(request.args.get("id"))
    result = Faculty.get_years(id)
    return {"response": result}, 200

# PROGRAMME ENDPOINTS


@programme_bp.route("/createprogramme", methods=["POST"])
def create_programme():
    name = request.args.get("name")
    faculty_id = int(request.args.get("facultyid"))
    if Programme.create(name, faculty_id):
        return {"response": "programme created"}, 200
    else:
        return {"response": "error"}, 500


@programme_bp.route("/updateprogramme", methods=["PUT"])
def update_programme():
    id = int(request.args.get("id"))
    name = request.args.get("name")
    faculty_id = int(request.args.get("facultyid"))
    if Programme.update(id, name, faculty_id):
        return {"response": "programme updated"}, 200
    else:
        return {"response": "error"}, 500


@programme_bp.route("/deleteprogramme", methods=["DELETE"])
def delete_programme():
    id = int(request.args.get("id"))
    if Programme.delete(id):
        return {"response": "programme deleted"}, 200
    else:
        return {"response": "error"}, 500


@programme_bp.route("/programmecourses", methods=["GET"])
def get_programme_courses():
    id = int(request.args.get("id"))
    year = int(request.args.get("year"))
    result = Programme.get_courses(id, year)
    return {"response": result}, 200
# COURSE ENDPOINTS


@course_bp.route("/createcourse", methods=["POST"])
def create_course():
    name = request.args.get("name")
    professor_id = request.args.get("professorid")
    room = request.args.get("room")
    start = request.args.get("start")
    f_start = datetime.strptime(start, '%H:%M').time()
    end = request.args.get("end")
    f_end = datetime.strptime(end, '%H:%M').time()
    day = request.args.get("day")
    week_type = request.args.get("wtype")
    year = int(request.args.get("year"))
    if Course.create(name, professor_id, room, f_start, f_end, day, week_type, year):
        return {"response": "course created"}, 200
    else:
        return {"response": "error"}, 500


@course_bp.route("/updatecourse", methods=["PUT"])
def update_course():
    id = int(request.args.get("id"))
    name = request.args.get('name')
    professor_id = request.args.get('professorid')
    room = request.args.get('room')
    start = request.args.get('start')
    f_start = datetime.strptime(start, '%H:%M').time()
    end = request.args.get('end')
    f_end = datetime.strptime(end, '%H:%M').time()
    day = request.args.get('day')
    week_type = request.args.get('wtype')
    year = int(request.args.get("year"))
    if Course.update(id, name, professor_id, room, f_start, f_end, day, week_type, year):
        return {"response": "course updated"}, 200
    else:
        return {"response": "error"}, 500


@course_bp.route("/deletecourse", methods=["DELETE"])
def delete_course():
    id = int(request.args.get("id"))
    if Course.delete(id):
        return {"response": "course deleted"}, 200
    else:
        return {"response": "error"}, 500


@course_bp.route("/courseprofessor", methods=["GET"])
def get_course_professor():
    id = int(request.args.get("id"))
    result = Professor.get_course_professor(id)
    return {"response": result}


# BASIC RATING ENDPOINTS


@basic_rating_bp.route("/insertbasic", methods=["POST"])
def insert_basic_rating():
    data = request.get_json()
    date = datetime.strptime(data["date"], "%d/%m/%Y %H:%M:%S")
    if BasicRating.create(data["rating"], data["room"], date):
        return {"response": "rating created"}, 200
    else:
        return {"response": "error"}, 500


@basic_rating_bp.route("/basicrange", methods=["GET"])
def retrieve_basic_daterange_mean():
    start = request.args.get('start')
    f_start = datetime.strptime(start, "%d/%m/%Y")
    end = request.args.get('end')
    f_end = datetime.strptime(end, "%d/%m/%Y")
    course_id = request.args.get("courseid")
    result = BasicRating.mean_per_day(f_start, f_end, course_id)
    return {"response": result}


@basic_rating_bp.route("/basictotal", methods=['GET'])
def retrieve_basic_total():
    course_id = request.args.get("courseid")
    result = BasicRating.total_mean(course_id)
    return {"response": result}


# COMPLEX RATING ENDPOINTS


@complex_rating_bp.route("/insertcomplex", methods=["POST"])
def insert_complex_rating():
    data = request.get_json()
    date = datetime.strptime(data["date"], "%d/%m/%Y %H:%M:%S")
    if ComplexRating.create(data["clarity"], data["interactivity"], data["relevance"], data["room"], date):
        return {"response": "rating created"}, 200
    else:
        return {"response": "error"}, 500


@complex_rating_bp.route("/complexrange", methods=["GET"])
def retrieve_complex_daterange_mean():
    start = request.args.get('start')
    f_start = datetime.strptime(start, "%d/%m/%Y")
    end = request.args.get('end')
    f_end = datetime.strptime(end, "%d/%m/%Y")
    course_id = request.args.get("courseid")
    result = ComplexRating.mean_per_day(f_start, f_end, course_id)
    return {"response": result}


@complex_rating_bp.route("/complextotal", methods=['GET'])
def retrieve_complex_total():
    course_id = request.args.get("courseid")
    result = ComplexRating.total_mean(course_id)
    return {"response": result}


# COURSE TO PROGRAMME ENDPOINTS


@prog_courses_bp.route("/coursetoprogramme", methods=["POST"])
def course_to_programme():
    course_id = int(request.args.get("courseid"))
    programme_id = int(request.args.get("programmeid"))
    if ProgrammeCourses.create(programme_id, course_id):
        return {"response": "relation created"}, 200
    else:
        return {"response": "error"}, 500


@course_bp.route("/deleteprogrammecourse", methods=["DELETE"])
def delete_programme_course():
    id = int(request.args.get("id"))
    if ProgrammeCourses.delete(id):
        return {"response": "course deleted"}, 200
    else:
        return {"response": "error"}, 500

# WEEK INTERVALS ENDPOINTS


@week_bp.route("/generateweeks", methods=["GET"])
def generate_weeks():
    Week.insert("03/10/2022", [12, 2, 2, 3, 1, 8, 1, 6])
    return {"response": "weeks generated"}, 200
