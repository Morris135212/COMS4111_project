from app import app
from flask import Flask, request, render_template, g, redirect, Response

from app.models import Course


@app.route("/courses")
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


