from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
CORS(app)

db = SQLAlchemy(app)

class Review(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  rating = db.Column(db.Integer)
  review = db.Column(db.String(200))
  created_at = db.Column(db.DateTime, default=datetime.datetime.now())

@app.route('/add_review', methods=['POST'])
def add_review():
  review_data = request.get_json()

  new_review = Review(rating=review_data['rating'], review=review_data['review'])

  db.session.add(new_review)
  db.session.commit()

  return 'Done', 201

@app.route('/reviews')
def reviews():
  review_list = Review.query.all()
  reviews = []

  for review in review_list:
    reviews.append({'rating':review.rating, 'review':review.review})

  return jsonify({'reviews': reviews})

if __name__=='__main__':
  app.run(debug=True)