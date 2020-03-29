from flask import Flask, render_template

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Use PyMongo to establish Mongo connection


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()
    
    #make auto generated table a bootstrap style table
    mars_data["Mars_Table"]=mars_data["Mars_Table"].replace('<table border="1" class="dataframe">',"<table class='table table-sm'>")
    
    print("--- MONGO DATA ---")
    print(mars_data)
    print("--- END MONGO DATA ---")
    # Return template and data
    return render_template("index.html", mission_mars=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/", 302)


if __name__ == "__main__":
    app.run(debug=True)