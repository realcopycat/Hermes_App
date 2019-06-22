"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, jsonify
from work1demo import app
from work1demo.requestProcess.firstRequest import req1Processor

@app.route('/')
@app.route('/home', methods=['get','post'])
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/firstsearch', methods=['get','post'])
def firstsearch():
    """Render Answer"""
    #print(request.args.get('caseDes'))
    answerDealer = req1Processor(request.args.get('caseDes'), request.args.get('caseLoc'))
    answer = answerDealer.main()
    return jsonify(answer)

    
    

