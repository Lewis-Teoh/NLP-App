import datetime
import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from tensorflow.keras.preprocessing.text import Tokenizer as KerasTokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from sentence_parser import Parser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
CORS(app)

db = SQLAlchemy(app)
MODEL = tf.keras.models.load_model('cp.h5')

def analyzerWrapper(review):
    X_list = []
    parser_obj = Parser(sent_segmenter=True)
    parser_obj.sent_to_doc(review)
    parsed_list = parser_obj.remove_punct()
    str_ = ""
    for idx_, list_ in enumerate(parsed_list):
        str_ += ' '.join(list_)
        str_ += ' '
    X_list.append(str_)
    
    X_copy = X_list.copy() 
    tk = KerasTokenizer(lower = True)
    tk.fit_on_texts(X_copy)
    X_seq = tk.texts_to_sequences(X_copy)
    X_pad = pad_sequences(X_seq, maxlen=200, padding='post')

    pred = MODEL.predict(X_pad, verbose=1)
    y_pred = np.argmax(pred,axis=-1)[0] # 0=pos , 1=neu, 2=neg according to training model format
    mapping = {
        0:'pos',
        1:'neu',
        2:'neg',
    }
    label = mapping[y_pred]
    return label

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    review = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    model_sentiment = db.Column(db.String(10))


@app.route('/add_review', methods=['POST'])
def add_review():
    review_data = request.get_json()
    
    try:
        label = analyzerWrapper(review_data['review'])
    except Exception as e:
        print(f"Failed to do prediction > {str(e)}")
        label = None

    new_review = Review(rating=review_data['rating'], review=review_data['review'], model_sentiment=label)

    db.session.add(new_review)
    db.session.commit()

    return 'Done', 201


@app.route('/reviews')
def reviews():
    review_list = Review.query.all()
    reviews = []

    for review in review_list:
        reviews.append({'rating': review.rating, 'review': review.review, 'model_sentiment': review.model_sentiment})

    return jsonify({'reviews': reviews})


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, threaded=False)
