from app import app, db
from app.models import User, Post

@app.shell_context_processor # function below invoked when 'flask shell' command runs
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

# if __name__ == "__main__":
#     app.run(threaded=True, debug=True)
# to be used if running 'python .\microblog.py'

# $env:FLASK_APP="microblog.py"