import iad
from flask import Flask, render_template, request, redirect


app = Flask(__name__)


@app.route('/')
def front():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def myapplication():
    if request.method == 'POST':

        f = request.files['userprofile']
        path = "./static/{}".format(f.filename)
        f.save(path)

        p = iad.sound_this_image(path)

        result_dic = {
            'image': path,
            'audio': p
        }

    return render_template("index.html", your_result = result_dic)


if __name__ == '__main__':
    app.run(debug=True)
