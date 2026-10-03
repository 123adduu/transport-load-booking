import os
from flask import Flask, render_template
from models import db
from routes.dashboard import dashboard_bp
from routes.vehicles import vehicles_bp
from routes.drivers import drivers_bp
from routes.loads import loads_bp
from routes.search import search_bp
from routes.assignments import assignments_bp
from routes.bookings import bookings_bp
from routes.import_data import import_data_bp

def create_app(test_config=None):
    """Application factory for Transport Load Booking System."""
    app = Flask(__name__, instance_relative_config=True)

    # Base configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'transport-load-booking-secure-key-2026'),
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'transport.db')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is not None:
        app.config.update(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(vehicles_bp)
    app.register_blueprint(drivers_bp)
    app.register_blueprint(loads_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(assignments_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(import_data_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500

    # Create tables automatically inside application context
    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
