from flask import render_template

from project import app


@app.route('/user/loadAbout')
def adminLoadAbout():
    return render_template('user/about.html')
