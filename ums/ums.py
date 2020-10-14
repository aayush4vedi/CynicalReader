"""Application entry point."""

from app_ums import create_app

app = create_app()

if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    app.run()

"""
1. Tell flask which app to run:  $ export FLASK_APP=ums.py
2. Enable debug mode for hot reloads:  $ export FLASK_DEBUG=1
3. Run the app: $ flask run
OR
just do $ bash start.sh
"""