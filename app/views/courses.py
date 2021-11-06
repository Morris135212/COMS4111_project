from app import app
from flask import Flask, request, render_template, g, redirect, Response

from app.models import Course, DataSets, University


@app.route("/courses", methods=["POST", "GET"])
def courses():
    sql = "SELECT * FROM courses"
    results = g.conn.execute(sql).fetchall()
    curriculums = []
    for i, result in enumerate(results):
        course = Course(*result)
        curriculums.append(course.__dict__)
    context = dict(courses=curriculums)
    print(context)
    return render_template("courses.html", **context)


@app.route("/course", methods=["POST", "GET"])
def course():
    c_id = request.form["c_id"]
    query_sql1 = "SELECT * FROM courses WHERE idx=%s"
    result = g.conn.execute(query_sql1, c_id).fetchall()
    print(result)
    c = Course(*result[0])
    query_sql2 = "SELECT d.name, d.idx, d.provenance " \
                 "FROM courses c " \
                 "INNER JOIN Explore e ON e.c_id=c.idx " \
                 "INNER JOIN Datasets d ON d.idx=e.d_id " \
                 "WHERE c.idx = %s"
    results = g.conn.execute(query_sql2, c_id).fetchall()
    datasets = []
    for i, result in enumerate(results):
        dataset = DataSets(*result)
        datasets.append(dataset.__dict__)

    query_sql3 = "SELECT u.name, u.location " \
                 "FROM UNIVERSITIES u " \
                 "INNER JOIN Teach t ON t.u_name = u.name " \
                 "INNER JOIN Courses c ON c.idx=t.c_id " \
                 "WHERE c.idx = %s"
    results = g.conn.execute(query_sql3, c_id).fetchall()
    universities = []
    for i, result in enumerate(results):
        uni = University(*result)
        universities.append(uni.__dict__)

    context = dict(course=c, datasets=datasets, universities=universities)
    return render_template("course.html", **context)