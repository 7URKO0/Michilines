from flask import Flask
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session

QUERY_TODOS_LOS_ALUMNOS = "SELECT nombre, apellido, padron FROM alumnos"

engine = create_engine("mysql://root:root@localhost:3306/test")

Session = scoped_session(sessionmaker(bind=engine))



app = Flask(__name__)

@app.route(rule='api/v1/alumnos', methods = ['GET'])
def get_todos_los_alumnos():
    return jsonify({'alumnos':'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True)