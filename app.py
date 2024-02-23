"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


connect_db(app)

@app.route('/')
def index_page():
    """Renders html template that includes some JS - NOT PART OF JSON API!"""
    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes=cupcakes)

@app.route('/api/cupcakes')
def list_cupcakes():
    """Returns JSON w/ all cupcakes"""
    all_cupcakes = [cupcakes.serialize() for cupcakes in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Returns JSON for one cupcake in particular"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Creates a new cupcake and returns JSON of that created cupcake"""
    data = request.json

    flavor = data.get('flavor')
    size = data.get('size')
    rating = data.get('rating')
    image = data.get('image', 'https://tinyurl.com/demo-cupcake')

    # Validate data (you can add more detailed validation if needed)
    if not all([flavor, size, rating]):
        return jsonify({"error": "Missing required data"}), 400

    new_cupcake = Cupcake(
        flavor=flavor,
        size=size,
        rating=rating,
        image=image
    )

    db.session.add(new_cupcake)
    db.session.commit()

    response_json = jsonify(cupcake=new_cupcake.serialize())
    return response_json, 201

@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """Updates a particular cupcake and responds w/ JSON of that updated cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """Deletes a particular cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")