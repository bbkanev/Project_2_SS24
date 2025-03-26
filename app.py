import os
from app import create_app, db

# Generate a secure secret key
secret_key = os.urandom(24)

# Create the Flask app using the factory function
app = create_app()

# Override the secret key configuration
app.config['SECRET_KEY'] = secret_key

if __name__ == '__main__':
    # Create all database tables
    with app.app_context():
        db.create_all()
    # Run the Flask application
    app.run(host="0.0.0.0", port=5000, debug=False)
