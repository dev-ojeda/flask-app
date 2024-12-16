import os
from dotenv import load_dotenv
from icecream import ic
from app import create_app,socketio

load_dotenv()
app = create_app()
def main():
    ic("Servidor Socket.IO ejecutándose en http://localhost:5000")
    socketio.run(app, debug=False, host=os.getenv("HOST"), port=os.getenv("PORT"), log_output=True,use_reloader=False)
if __name__ == '__main__':
    # socketio.run(app, debug=True)
    main()