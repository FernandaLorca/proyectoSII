from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import psycopg2.extras
import os


app=Flask(__name__)

def connectDB():
    connectionString='dbname=proyectosii user=fer password=ferfer host=localhost'
    print(connectionString)
    try:
        return psycopg2.connect(connectionString)
    except:
        print("No se pudo conectar.")

@app.route('/')
def index():
    conectar = connectDB()
    cursor = conectar.cursor()
    cursor.execute("""SELECT factor FROM IA_2022;""")
    
    ans=cursor.fetchall()

    return render_template('index.html', ans=ans)

@app.route('/pagina')
def pagina():
    var = 'Esta es la pagina secundaria'
    return render_template('pagina.html', var=var)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method=='GET':
        return render_template('admin_login.html')
    else:
        user = request.form.get("password")

        if user=='sii123':
        
            conectar = connectDB()
            cursor=conectar.cursor()
            cursor.execute(f"""SELECT c.rut, c.nombre, c.edad, count(p.rut_cliente)
                            FROM cliente AS c, pedido AS p
                            WHERE c.rut='{user}'
                            AND c.rut=p.rut_cliente
                            GROUP BY c.rut;""")

            cliente=cursor.fetchall()

        if cliente :

            conectar = connectDB()
            cursor=conectar.cursor()
            cursor.execute(f"""SELECT DISTINCT(t.nombre)
                            FROM cliente AS c, trabajador as t, tra_cli as tc
                            WHERE c.rut='{user}'
                            AND c.rut=tc.rut_cliente 
                            AND t.id_trabajador = tc.id_trabajador;""")
            
            trabajadores=cursor.fetchall()

            conectar = connectDB()
            cursor=conectar.cursor()
            cursor.execute(f"""SELECT SUM(f.total)
                            FROM factura AS f, pedido as p, cliente AS c
                            WHERE c.rut=p.rut_cliente 
                            AND f.codigo_pedido = p.codigo_pedido
                            AND c.rut='{user}';""")
            
            total=cursor.fetchall()

            ctx = {
            "cliente" : cliente,
            "trabajadores" : trabajadores,
            "total" : total
            }
            
            return render_template('index_cliente.html', contexto=ctx)

        else:
            flash('Rut invalido', 'warning')
            return redirect(url_for('cliente'))

if __name__ == '__main__':
    app.run()