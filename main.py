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


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method=='GET':
        return render_template('admin_login.html')
    else:

        user = request.form.get("password")

        if user=='sii123':

            conectar = connectDB()
            cursor=conectar.cursor()
            cursor.execute("""SELECT desde, hasta, factor, CR
                            FROM IA_2022; """)
        
            datos=cursor.fetchall()

            conectar = connectDB()
            cursor=conectar.cursor()
            cursor.execute("""SELECT mes_v, porcentaje
                            FROM CM_2021
                            WHERE mes_h='Diciembre'; """)

            cm=cursor.fetchall()

            ctx = {
            "datos" : datos,
            "cm" : cm
            }

            return render_template('admin.html', contexto=ctx)

        else:
             return render_template('index.html')


if __name__ == '__main__':
    app.run()