from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from flask_wtf import CSRFProtect
import psycopg2
import psycopg2.extras
import os


app = Flask(__name__)
app.secret_key = 'my_secret_key'
csrf = CSRFProtect(app)


def connectDB():
    connectionString='dbname=taxhelp user=cata password=catacata host=localhost'
    print(connectionString)
    try:
        return psycopg2.connect(connectionString)
    except:
        print("No se pudo conectar.")

@app.route('/')
def index():

    conectar = connectDB()
    cursor=conectar.cursor()
    cursor.execute("""SELECT distinct anio FROM IA;""")
        
    anios=cursor.fetchall()

    return render_template('index.html', anios=anios)

@app.route('/admin')
def admin():

    if 'user' in session:
        user = session['user']
        print (user)

        conectar = connectDB()
        cursor=conectar.cursor()
        cursor.execute("""SELECT desde, hasta, factor, CR, anio
                        FROM IA order by anio, factor; """)
        
        datos=cursor.fetchall()

        conectar = connectDB()
        cursor=conectar.cursor()
        cursor.execute("""SELECT mes, porcentaje, anio
                        FROM CM order by anio; """)

        cm=cursor.fetchall()

        ctx = {
        "datos" : datos,
        "cm" : cm
        }

        return render_template('admin.html', contexto=ctx)

    else:
        return redirect('adminlogin')

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():

    if request.method == 'POST':
        user = request.form.get("password")
        if user == 'sii123':
            session['user'] = request.form.get("password")


            conectar = connectDB()
            cursor=conectar.cursor()
            cursor.execute("""SELECT desde, hasta, factor, CR, anio
                            FROM IA order by anio, factor; """)
        
            datos=cursor.fetchall()

            conectar = connectDB()
            cursor=conectar.cursor()
            cursor.execute("""SELECT mes, porcentaje, anio
                            FROM CM order by anio; """)

            cm=cursor.fetchall()

            ctx = {
            "datos" : datos,
            "cm" : cm
            }

            return render_template('admin.html', contexto=ctx)

        else:
            success_message = 'Contraseña Incorrecta'
            flash(success_message)
            return redirect('admin')

    return render_template('adminlogin.html')

@app.route('/logout')
def logout():

    if 'user' in session:
        session.pop('user')
      
    return redirect(url_for('index'))

@app.route('/calculo/<int:anio>')
def calculo(anio):

    conectar = connectDB()
    cursor=conectar.cursor()
    cursor.execute(f"""SELECT * FROM IA WHERE anio={anio};""")
        
    ans=cursor.fetchall()
   
    return render_template('calculo.html', ans=ans)


@app.route('/ingresarcm', methods=['GET', 'POST'])
def ingresarcm():

    if request.method=='GET':
        return render_template('ingresarcm.html')

    else:

        mes = request.form.get("mes")
        porcentaje = request.form.get("porcentaje")
        anio = request.form.get("anio")

        sql = 'INSERT INTO CM (mes, porcentaje, anio) VALUES(%s,%s,%s)'

        datos = (mes, porcentaje, anio)

        conectar = connectDB()
        cursor=conectar.cursor()

        print(sql)

        try:
            cursor.execute(sql,datos)
            conectar.commit()
            success_message = 'Dato ingresado exitosamente.'
            flash(success_message)
            return redirect('/admin')
        except:
            success_message = 'Dato no ingresado. Verifique que no exista un dato con el mismo mes y año.'
            flash(success_message)
            return redirect('/ingresarcm')
    

@app.route('/ingresaria', methods=['GET', 'POST'])
def ingresaria():

    if request.method=='GET':
        return render_template('ingresaria.html')

    else:

        desdeIA = request.form.get("desdeIA")
        hastaIA = request.form.get("hastaIA")
        factorIA = request.form.get("factorIA")
        cr = request.form.get("CR")
        anio = request.form.get("anio")

        sql = 'INSERT INTO IA (desde, hasta, factor, CR, anio) VALUES(%s,%s,%s,%s,%s)'

        datos = (desdeIA, hastaIA, factorIA, cr, anio)

        conectar = connectDB()
        cursor=conectar.cursor()

        print(sql)

        try:
            cursor.execute(sql,datos)
            conectar.commit()
            success_message = 'Dato ingresado exitosamente.'
            flash(success_message)
            return redirect('/admin')
        except:
            success_message = 'Dato no ingresado. Verifique que no exista un dato con el mismo factor y año.'
            flash(success_message)
            return redirect('/ingresaria')

@app.route('/eliminaria', methods=['GET', 'POST'])
def eliminaria():

    conectar = connectDB()
    cursor=conectar.cursor()
    cursor.execute("""SELECT desde, hasta, factor, CR, anio
                            FROM IA order by anio, factor; """)
        
    datos=cursor.fetchall()

    conectar = connectDB()
    cursor=conectar.cursor()
    cursor.execute("""SELECT mes, porcentaje, anio
                       FROM CM order by anio; """)

    cm=cursor.fetchall()

    ctx = {
        "datos" : datos,
        "cm" : cm
            }

    if request.method=='GET':
        return render_template('eliminaria.html', contexto=ctx)

    else:

        desdeIA = request.form.get("desdeIA")
        hastaIA = request.form.get("hastaIA")
        factorIA = request.form.get("factorIA")
        cr = request.form.get("CR")
        anio = request.form.get("anio")

        sql = 'DELETE FROM IA WHERE desde=%s AND hasta=%s AND factor=%s AND CR=%s AND anio=%s'

        datos = (desdeIA, hastaIA, factorIA, cr, anio)

        conectar = connectDB()
        cursor=conectar.cursor()

        print(sql)

        try:
            cursor.execute(sql,datos)
            conectar.commit()
            success_message = 'Dato eliminado exitosamente.'
            flash(success_message)
            return redirect('/admin')
        except:
            success_message = 'Dato no eliminado. Verifique los valores ingresados.'
            flash(success_message)
            return redirect('/eliminaria')
        

@app.route('/eliminarcm', methods=['GET', 'POST'])
def eliminarcm():

    conectar = connectDB()
    cursor=conectar.cursor()
    cursor.execute("""SELECT desde, hasta, factor, CR, anio
                            FROM IA order by anio, factor; """)
        
    datos=cursor.fetchall()

    conectar = connectDB()
    cursor=conectar.cursor()
    cursor.execute("""SELECT mes, porcentaje, anio
                       FROM CM order by anio; """)

    cm=cursor.fetchall()

    ctx = {
        "datos" : datos,
        "cm" : cm
            }

    if request.method=='GET':
        return render_template('eliminarcm.html', contexto=ctx)

    else:

        mes = request.form.get("mes")
        porcentaje = request.form.get("porcentaje")
        anio = request.form.get("anio")

        sql = 'DELETE FROM CM WHERE mes=%s AND porcentaje=%s AND anio=%s'

        datos = (mes, porcentaje, anio)

        conectar = connectDB()
        cursor=conectar.cursor()

        print(sql)

        try:
            cursor.execute(sql,datos)
            conectar.commit()
            success_message = 'Dato eliminado exitosamente.'
            flash(success_message)
            return redirect('/admin')
        except:
            success_message = 'Dato no eliminado. Verifique los valores ingresados.'
            flash(success_message)
            return redirect('/eliminarcm')

@app.route('/calcular',  methods=['POST'])
def calcular():

    
   
    return render_template('calcular.html')

if __name__ == '__main__':
    app.run(debug=True)