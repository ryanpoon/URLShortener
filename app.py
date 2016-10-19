import string, random
from flask import Flask, request, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Text, Integer, update

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)
app.debug = True

BASE_URL = '127.0.0.1:5000'

class UrlObject(db.Model):
    Url = Column(Text, unique=False)
    Code = Column(Text, primary_key=True)
    Views = Column(Integer, unique=False, default=1)

    def __init__(self, url, code):
        self.Url = url
        self.Code = code
        self.Views = 1

def id_generator(url, size=6, chars=string.ascii_uppercase + string.digits):
    random.seed(url)
    return ''.join(random.choice(chars) for _ in range(size))


@app.route('/')
def home():
    print UrlObject.query.all()
    return render_template('home.html')


@app.route('/get_url')
def get_url():
    url = request.args.get('url', '')
    custom = request.args.get('code', '')
    if UrlObject.query.filter_by(Code=custom).first():
        return jsonify(result='http://127.0.0.1:5000/'+custom)
    elif custom:
        code = custom
    else:
        code = id_generator(url)

    u =  UrlObject.query.filter_by(Url = url).first()
    if u:
        code = id_generator(url)
        if code == u.Code:
            return jsonify(result='http://127.0.0.1:5000/'+code, views = u.Views)
        else:
            return jsonify(result='http://127.0.0.1:5000/'+u.Code, views = u.Views)


    urlobject = UrlObject(url, code)
    db.session.add(urlobject)
    db.session.commit()
    print "Yo",urlobject
    return jsonify(result='http://127.0.0.1:5000/'+code, views = urlobject.Views)


@app.route('/<code>', methods=['GET'])
def get_redirect(code):
    url = UrlObject.query.filter_by(Code=code).first()

    if url:
        url.Views += 1
        db.session.commit()
        return redirect(url.Url)
    else:
        return render_template('doesnotexist.html')



if __name__ == "__main__":
    app.run()