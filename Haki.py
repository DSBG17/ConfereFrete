from flask import Flask, render_template

app = Flask (__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/calculos')
def calculo():
    return render_template ("calculos.html")

@app.route('/varredura')
def varredura():
    return render_template("varredura.html")

@app.route('/extrato')
def extrato():
    return render_template("extrato.html")

if __name__ == "__main__":
    app.run(debug=True)