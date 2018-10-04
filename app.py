# import necessary libraries
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape

# create instance of Flask app
app = Flask(__name__)

conn = 'mongodb://localhost:27017'
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# create mongo connection
#client = PyMongo.MongoClient()
db = mongo.db.mars_db
collection = db.mars_data_entries
mars_data = scrape.scrape()
db.update({}, mars_data, upsert=True)

@app.route("/")
def home():
    mars_data = mongo.db.mars_db.find_one()
    print(mars_data)
    return render_template('index.html', mars_data=mars_data)

@app.route("/scrape")
def web_scrape():
    db.collection.remove({})
    mars_data = scrape.scrape()
    db.update({}, mars_data, upsert=True)

    return  render_template('index.html', mars_data=mars_data)

if __name__ == "__main__":
    app.run(debug=True)
