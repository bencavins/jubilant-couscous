from flask import Flask, render_template
from .models import DB, User, Tweet

def create_app():
    app = Flask(__name__)
    app_title = "Twitoff DS38"

    # Database config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)

    @app.route("/")
    def root():
        return render_template('base.html', title='Home')

    @app.route("/test")
    def test():
        return f"<p>This is a page for {app_title}</p>"
    
    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()
        return """The database has been reset
        <a href='/'>Go to Home</a>
        <a href='/reset'>Go to reset</a>
        <a href='/populate'>Go to populate</a>
        """
    
    @app.route("/populate")
    def populate():
        user1 = User(id=1, username='ben')
        DB.session.add(user1)
        user2 = User(id=2, username='adam')
        DB.session.add(user2)
        tweet = Tweet(id=1, text='This is my tweet', user=user1)
        DB.session.add(tweet)
        DB.session.commit()
        return """The database has been reset
        <a href='/'>Go to Home</a>
        <a href='/reset'>Go to reset</a>
        <a href='/populate'>Go to populate</a>
        """
    
    return app