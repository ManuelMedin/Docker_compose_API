import time
import psycopg2
from flask import Flask


app = Flask(__name__)




def crearTablaConFila():
  conexion = psycopg2.connect(host="172.19.0.1",user="admin",password="admin",database="postgres",port="5432")
  cur = conexion.cursor()
  query = "CREATE TABLE IF NOT EXISTS contador (valor int)"
  cur.execute(query)
  conexion.commit()
  query="DO $$ declare BEGIN IF ((SELECT COUNT(*) FROM contador)<1) THEN INSERT INTO contador values(0); END IF; end $$"
  cur.execute(query)
  conexion.commit()
  cur.close()
  conexion.close()

def sumarContador():
  conexion = psycopg2.connect(host="172.19.0.1",user="admin",password="admin",database="postgres",port="5432")
  cur = conexion.cursor()
  query="UPDATE contador SET valor=(SELECT SUM(valor+1) FROM contador)"
  cur.execute(query)
  conexion.commit()
  cur.close()
  conexion.close()

def get_hit_count():
  crearTablaConFila()
  sumarContador()
  retries = 5
  while True:
    try: 
      query="SELECT * FROM contador LIMIT 1 OFFSET 0"
      conexion = psycopg2.connect(host="172.19.0.1",user="admin",password="admin",database="postgres",port="5432")
      cur = conexion.cursor()
      cur.execute(query)
      visitasAlSitio=cur.fetchall()
      visitasAlSitio=visitasAlSitio[0][0]
      print (visitasAlSitio)
      cur.close()
      conexion.close()
      return visitasAlSitio
      
    except Exception as error:
      if retries == 0:
        raise error
      retries -= 1
      time.sleep(0.5)

def reiniciarValores():
  conexion = psycopg2.connect(host="172.19.0.1",user="admin",password="admin",database="postgres",port="5432")
  cur = conexion.cursor()
  query="UPDATE contador SET valor=0"
  cur.execute(query)
  conexion.commit()
  cur.close()
  conexion.close()

def alterarValores(valorAlterado):
  conexion = psycopg2.connect(host="172.19.0.1",user="admin",password="admin",database="postgres",port="5432")
  cur = conexion.cursor()
  query=("UPDATE contador SET valor=" + str(valorAlterado))
  cur.execute(query)
  conexion.commit()
  cur.close()
  conexion.close()


@app.route('/', methods=['GET'])
def hello():
  count = get_hit_count()
  return 'Hello World! I have been seen {} times.\n'.format(count)

@app.route('/reiniciar', methods=['DELETE'])
def reiniciarContador():
  reiniciarValores()
  return 'El contador se ha reiniciado correctamente'

@app.route('/modificar/<valorModificado>', methods=['PUT','POST'])
def modificarContador(valorModificado):
  alterarValores(valorModificado)
  return 'El contador se ha alterado correctamente'