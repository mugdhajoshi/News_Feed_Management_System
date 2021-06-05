# Importing The Required Libraries
from flask import Flask, render_template, request
from flask_pymongo import PyMongo

# Create the application
app = Flask(__name__)

# Creating Connection to MongoDB
app.config['MONGO_DBNAME'] = 'collection'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/news_intellimind'
mongo = PyMongo(app)


@app.route('/')
def index():
    """
        Displays the index page accessible at '/'
    """
    return render_template('index.html')


@app.route('/search_for_keyword', methods=['GET', 'POST'])
def find():
    """
        Display articles based on keyword provided in the input
    """
    required_article = []
    if request.method == 'POST':
        # Taking keyword from the input named 'key'
        keyword = request.form['key']
        # Finding the keyword in the document
        news = mongo.db.collection.find()
        # Storing all the fetched news in required_article string
        for record in news:
            if keyword.lower() in record['body'].lower():
                required_article.append(record['body'])
    content1 = required_article
    return render_template('table0.html', content1=content1)


@app.route('/count_of_article_captured_by_source', methods=['GET', 'POST'])
def article_by_source():
    """
        Display Count of articles captured by source
    """

    dic1 = {}
    if request.method == 'POST':
        news = mongo.db.collection.find()
        for record in news:
            if record['source'] in dic1:
                dic1[record['source']] += 1
            else:
                dic1[record['source']] = 1
    return render_template('table1.html', dic1=dic1)


@app.route('/count_of_article_captured_by_source_and_date', methods=['GET', 'POST'])
def article_by_source_and_date():
    """
        Display Count of articles captured by source and date
    """

    dic2 = {}
    if request.method == 'POST':
        news = mongo.db.collection.find()
        for record in news:
            if record['source'] + "!@#$%^" + record['story_date'] in dic2:
                dic2[record['source'] + "!@#$%^" + record['story_date']] += 1
            else:
                dic2[record['source'] + "!@#$%^" + record['story_date']] = 1
    dic2 = dic2
    return render_template('table2.html', dic2=dic2)


@app.route('/duplicity_of_feed_by_title_story_date', methods=['GET', 'POST'])
def checking_duplicity():
    """
        Duplicity of feed by title and story date
    """

    dic3 = {}
    result = []
    if request.method == 'POST':
        news = mongo.db.collection.find()
        for record in news:
            if record['title'] + "!@#$%^" + record['story_date'] in dic3:
                result.append(record['title'])
                dic3[record['title'] + "!@#$%^" + record['story_date']] += 1
            else:
                dic3[record['title'] + "!@#$%^" + record['story_date']] = 1
    return render_template('table3.html', result=result)


if __name__ == "__main__":
    app.run(debug=True)
