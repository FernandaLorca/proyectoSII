from termios import CR3
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import psycopg2.extras
import os


app=Flask(__name__)

def connectDB():
    connectionString='dbname=taxhelp user=fer password=ferfer host=localhost'
    print(connectionString)
    try:
        return psycopg2.connect(connectionString)
    except:
        print("No se pudo conectar.")

@app.route('/')
def index():
    conectar = connectDB()
    cursor = conectar.cursor()
    cursor.execute("""SELECT factor FROM IA;""")
    
    ans=cursor.fetchall()

    return render_template('index.html', ans=ans)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method=='GET':
        return render_template('adminLog.html')
    else:

        user = request.form.get("password")

        if user=='sii123':

            conectar = connectDB()
            cursor=conectar.cursor()
            cursor.execute("""SELECT desde, hasta, factor, CR, anio
                            FROM IA; """)
        
            datos=cursor.fetchall()

            conectar = connectDB()
            cursor=conectar.cursor()
            cursor.execute("""SELECT mes, porcentaje, anio
                            FROM CM; """)

            cm=cursor.fetchall()

            ctx = {
            "datos" : datos,
            "cm" : cm
            }

            return render_template('admin.html', contexto=ctx)

        else:
             return render_template('index.html')

@app.route('/crearCM', methods=['GET', 'POST'])
def crearCM():
    if request.method=='GET':
        return render_template('añadirCM.html')
    else:

        enero = request.form.get("P.enero")
        febrero = request.form.get("P.febrero")
        marzo = request.form.get("P.marzo")
        abril = request.form.get("P.abril")
        mayo = request.form.get("P.mayo")
        junio = request.form.get("P.junio")
        julio = request.form.get("P.julio")
        agosto = request.form.get("P.agosto")
        septiembre = request.form.get("P.septiembre")
        octubre = request.form.get("P.octubre")
        noviembre = request.form.get("P.noviembre")
        anio = request.form.get("anio")
        
        conectar = connectDB()
        cursor=conectar.cursor()
        cursor.execute(f"""insert into CM (mes,  porcentaje, anio) values ('Enero', {enero}, {anio}); """)
        cursor.execute(f"""insert into CM (mes,  porcentaje, anio) values ('Enero', {febrero}, {anio}); """)
        cursor.execute(f"""insert into CM (mes,  porcentaje, anio) values ('Enero', {marzo}, {anio}); """)
        cursor.execute(f"""insert into CM (mes,  porcentaje, anio) values ('Enero', {abril}, {anio}); """)
        cursor.execute(f"""insert into CM (mes,  porcentaje, anio) values ('Enero', {mayo}, {anio}); """)
        cursor.execute(f"""insert into CM (mes,  porcentaje, anio) values ('Enero', {junio}, {anio}); """)
        cursor.execute(f"""insert into CM (mes,  porcentaje, anio) values ('Enero', {julio}, {anio}); """)
        cursor.execute(f"""insert into CM (mes,  porcentaje, anio) values ('Enero', {agosto}, {anio}); """)
        cursor.execute(f"""insert into CM (mes,  porcentaje, anio) values ('Enero', {septiembre}, {anio}); """)
        cursor.execute(f"""insert into CM (mes,  porcentaje, anio) values ('Enero', {octubre}, {anio}); """)
        cursor.execute(f"""insert into CM (mes,  porcentaje, anio) values ('Enero', {noviembre}, {anio}); """)

    
        return render_template('admin.html')

@app.route('/crearIA', methods=['GET', 'POST'])
def crearIA():
    if request.method=='GET':
        return render_template('añadirIA.html')
    else:
        #desde = []
        #for i in range (8):
        #    desde[i+1] = request.form.get("desde"+[i+1])

        desde1 = request.form.get("desde1")
        desde2 = request.form.get("desde2")
        desde3 = request.form.get("desde3")
        desde4 = request.form.get("desde4")
        desde5 = request.form.get("desde5")
        desde6 = request.form.get("desde6")
        desde7 = request.form.get("desde7")
        desde8 = request.form.get("desde8")

        hasta1 = request.form.get("hasta1")
        hasta2 = request.form.get("hasta2")
        hasta3 = request.form.get("hasta3")
        hasta4 = request.form.get("hasta4")
        hasta5 = request.form.get("hasta5")
        hasta6 = request.form.get("hasta6")
        hasta7 = request.form.get("hasta7")
        #hasta8 = request.form.get("hasta8")

        factor1 = request.form.get("factor1")
        factor2 = request.form.get("factor2")
        factor3 = request.form.get("factor3")
        factor4 = request.form.get("factor4")
        factor5 = request.form.get("factor5")
        factor6 = request.form.get("factor6")
        factor7 = request.form.get("factor7")
        factor8 = request.form.get("factor8")

        cr1 = request.form.get("factor1")
        cr2 = request.form.get("factor2")
        cr3 = request.form.get("factor3")
        cr4 = request.form.get("factor4")
        cr5 = request.form.get("factor5")
        cr6 = request.form.get("factor6")
        cr7 = request.form.get("factor7")
        cr8 = request.form.get("factor8")

        anio = request.form.get("anio")
        
        conectar = connectDB()
        cursor=conectar.cursor()

        cursor.execute(f"""insert into IA (desde, hasta, factor, CR, anio) values ({desde1}, {hasta1}, {factor1}, {cr1}, {anio});""")
        cursor.execute(f"""insert into IA (desde, hasta, factor, CR, anio) values ({desde2}, {hasta2}, {factor2}, {cr2}, {anio});""")
        cursor.execute(f"""insert into IA (desde, hasta, factor, CR, anio) values ({desde3}, {hasta3}, {factor3}, {cr3}, {anio});""")
        cursor.execute(f"""insert into IA (desde, hasta, factor, CR, anio) values ({desde4}, {hasta4}, {factor4}, {cr4}, {anio});""")
        cursor.execute(f"""insert into IA (desde, hasta, factor, CR, anio) values ({desde5}, {hasta5}, {factor5}, {cr5}, {anio});""")
        cursor.execute(f"""insert into IA (desde, hasta, factor, CR, anio) values ({desde6}, {hasta6}, {factor6}, {cr6}, {anio});""")
        cursor.execute(f"""insert into IA (desde, hasta, factor, CR, anio) values ({desde7}, {hasta7}, {factor7}, {cr7}, {anio});""")
        cursor.execute(f"""insert into IA (desde, hasta, factor, CR, anio) values ({desde8}, null, {factor8}, {cr8}, {anio});""")


        conectar.commit()
        print("Records inserted successfully")
        conectar.close()
    
        return render_template('admin.html')


if __name__ == '__main__':
    app.run()