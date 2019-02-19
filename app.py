from flask import Flask,render_template, request
from Parser import parser
from Parser import twitter
import pandas as pd
from IPython.display import HTML


app = Flask(__name__, static_url_path='')
symbol = ""
company_name = ""

@app.route('/home/')
def root():
    return app.send_static_file('main.html')

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/submit',methods=['POST'])
def submit():
    if request.method == 'POST':
        global symbol
        symbol = request.form['comment']
        data = (parser.transcripts(symbol))[0]
        global company_name
        company_name = data
    return render_template('main.html', company = data)

@app.route('/transcripts',methods=['POST'])
def transcripts():
    data = []
    if request.method == 'POST':
        data = parser.transcripts(symbol)
    headers = []
    for i in range(3, len(data)):
        if len(data[i].split(' ')) <= 3:
            headers.append(i - 2)
    return render_template('transcripts.html', trans = data, trans2 = data[3:], headers = headers)

@app.route('/prices',methods=['POST'])
def prices():
    data = ()
    if request.method == 'POST':
        data = parser.prices(symbol)
    return render_template('prices.html', stock_price = data[0], stock_rate = data[1], stock_percent = data[2],
                           stock_trend = data[3], incr = data[4], company_name = company_name)

@app.route('/news',methods=['POST'])
def news():
    data = ()
    if request.method == 'POST':
        data = parser.prices(symbol)
    return render_template('prices.html', company_name = company_name)

@app.route('/numbers',methods=['POST'])
def numbers():
    data = ()
    if request.method == 'POST':
        data = parser.prices(symbol)
    return render_template('prices.html', company_name = company_name)

@app.route('/media',methods=['POST'])
def media():
    if request.method == 'POST':
        data = twitter.search_tweets(company_name[:len(company_name) - 3 - len(symbol)])
    with pd.option_context('display.max_colwidth', -1): output_html = data.to_html(index = False)
    return render_template('media.html', company_name = company_name, tweets = output_html)

if __name__ == '__main__':
    app.run(debug=True)