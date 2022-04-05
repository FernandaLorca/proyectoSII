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
from datetime import date


app = Flask(__name__)
app.secret_key = 'my_secret_key'
csrf = CSRFProtect(app)


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

            return redirect('/admin')

        else:
            success_message = 'Contraseña Incorrecta. Intente nuevamente.'
            flash(success_message)
            return redirect('admin')

    return render_template('adminlogin.html')

@app.route('/logout')
def logout():

    if 'user' in session:
        session.pop('user')
        success_message = 'Sesión cerrada exitosamente.'
        flash(success_message)
      
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

    if 'user' in session:

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
        
    else: 
        success_message = 'Inicie sesión para acceder al panel de administración.'
        flash(success_message)
        return redirect(url_for('adminlogin'))
    

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

@app.route('/resultados/<int:anio>',  methods=['POST'])
def resultados(anio):

    SIEnero = request.form.get("SIEnero")
    IREnero = request.form.get("IREnero")
    HBEnero = request.form.get("HBEnero")
    HREnero = request.form.get("HREnero")

    SIFebrero = request.form.get("SIFebrero")
    IRFebrero = request.form.get("IRFebrero")
    HBFebrero = request.form.get("HBFebrero")
    HRFebrero = request.form.get("HRFebrero")

    SIMarzo = request.form.get("SIMarzo")
    IRMarzo = request.form.get("IRMarzo")
    HBMarzo = request.form.get("HBMarzo")
    HRMarzo = request.form.get("HRMarzo")

    SIAbril = request.form.get("SIAbril")
    IRAbril = request.form.get("IRAbril")
    HBAbril = request.form.get("HBAbril")
    HRAbril = request.form.get("HRAbril")

    SIMayo = request.form.get("SIMayo")
    IRMayo = request.form.get("IRMayo")
    HBMayo = request.form.get("HBMayo")
    HRMayo = request.form.get("HRMayo")

    SIJunio = request.form.get("SIJunio")
    IRJunio = request.form.get("IRJunio")
    HBJunio = request.form.get("HBJunio")
    HRJunio = request.form.get("HRJunio")

    SIJulio = request.form.get("SIJulio")
    IRJulio = request.form.get("IRJulio")
    HBJulio = request.form.get("HBJulio")
    HRJulio = request.form.get("HRJulio")

    SIAgosto = request.form.get("SIAgosto")
    IRAgosto = request.form.get("IRAgosto")
    HBAgosto = request.form.get("HBAgosto")
    HRAgosto = request.form.get("HRAgosto")

    SISeptiembre = request.form.get("SISeptiembre")
    IRSeptiembre = request.form.get("IRSeptiembre")
    HBSeptiembre = request.form.get("HBSeptiembre")
    HRSeptiembre = request.form.get("HRSeptiembre")

    SIOctubre = request.form.get("SIOctubre")
    IROctubre = request.form.get("IROctubre")
    HBOctubre = request.form.get("HBOctubre")
    HROctubre = request.form.get("HROctubre")

    SINoviembre = request.form.get("SINoviembre")
    IRNoviembre = request.form.get("IRNoviembre")
    HBNoviembre = request.form.get("HBNoviembre")
    HRNoviembre = request.form.get("HRNoviembre")

    SIDiciembre = request.form.get("SIDiciembre")
    IRDiciembre = request.form.get("IRDiciembre")
    HBDiciembre = request.form.get("HBDiciembre")
    HRDiciembre = request.form.get("HRDiciembre")



    SI = [SIEnero,SIFebrero,SIMarzo,SIAbril,SIMayo,SIJunio,SIJulio,SIAgosto,SISeptiembre,SIOctubre,SINoviembre,SIDiciembre]
    IR = [IREnero,IRFebrero,IRMarzo,IRAbril,IRMayo,IRJunio,IRJulio,IRAgosto,IRSeptiembre,IROctubre,IRNoviembre,IRDiciembre]
    HB = [HBEnero,HBFebrero,HBMarzo,HBAbril,HBMayo,HBJunio,HBJulio,HBAgosto,HBSeptiembre,HBOctubre,HBNoviembre,HBDiciembre]
    HR = [HREnero,HRFebrero,HRMarzo,HRAbril,HRMayo,HRJunio,HRJulio,HRAgosto,HRSeptiembre,HROctubre,HRNoviembre,HRDiciembre]

    datos = [   [1,SIEnero,IREnero,HBEnero,HREnero],
                [2,SIFebrero,IRFebrero,HBFebrero,HRFebrero],
                [3,SIMarzo,IRMarzo,HBMarzo,HRMarzo],
                [4,SIAbril,IRAbril,HBAbril,HRAbril],
                [5,SIMayo,IRMayo,HBMayo,HRMayo],
                [6,SIJunio,IRJunio,HBJunio,HRJunio],
                [7,SIJulio,IRJulio,HBJulio,HRJulio],
                [8,SIAgosto,IRAgosto,HBAgosto,HRAgosto],
                [9,SISeptiembre,IRSeptiembre,HBSeptiembre,HRSeptiembre],
                [10,SIOctubre,IROctubre,HBOctubre,HROctubre],
                [11,SINoviembre,IRNoviembre,HBNoviembre,HRNoviembre],
                [12,SIDiciembre,IRDiciembre,HBDiciembre,HRDiciembre],
            ]  

     ########## CÁLCULOS ##########

    flagProyeccion = False # True si corresponde hacer proyeccion
    mesProyeccion = 0
    filanula=0
    contador_filasnulas=0

    for i in range(12):
        filanula=0
        for j in range(5):
            if datos[i][j] == None or datos[i][j] == '':
                filanula = filanula+1
            
            if filanula==4:
                flagProyeccion=True
                contador_filasnulas=contador_filasnulas+1
                if mesProyeccion==0:
                    mesProyeccion = i
                
            if filanula==0 and flagProyeccion==True and (datos[i-1][j]== ' ' or datos[i-1][j]== None):
                print(i,'se cae en el primer if')
                success_message = 'Error. Por favor verifique las indicaciones e ingrese los datos correctamente.'
                flash(success_message)
                return redirect(f'/calculo/{anio}')  #error   
         
        if filanula>0 and filanula<4:
            print('se cae en el segundo if')
            success_message = 'Error. Por favor verifique las indicaciones e ingrese los datos correctamente.'
            flash(success_message)
            return redirect(f'/calculo/{anio}')  #error  
        
        if(contador_filasnulas==12):
                success_message = 'ERROR. Por favor ingrese al menos un mes de renta.'
                flash(success_message)
                return redirect(f'/calculo/{anio}') 

        else:
            if(datos[i][1].isnumeric() and datos[i][2].isnumeric()):
                Imponible= float(datos[i][1])
                Retenido=float(datos[i][2])
                if(Imponible<Retenido):
                    success_message = 'ERROR. Los impuestos retenidos no pueden ser mayores al sueldo imponible y/o honorario bruto por mes.'
                    flash(success_message)
                    return redirect(f'/calculo/{anio}')  #error
            if(datos[i][3].isnumeric() and datos[i][4].isnumeric()):
                Imponible= float(datos[i][3])
                Retenido=float(datos[i][4])
                if(Imponible<Retenido):
                    success_message = 'ERROR. Los impuestos retenidos no pueden ser mayores al sueldo imponible y/o honorario bruto por mes.'
                    flash(success_message)
                    return redirect(f'/calculo/{anio}')  #error


    flagIngresos = False # True si percibe los dos tipos de ingresos
    flagTipoIngreso = False # True si el tipo de ingreso es salario
    SA = 0
    HA = 0
    for index in range(12):
        if (SI[index].isnumeric()):
            SA = SA + float(SI[index])
        if (HB[index].isnumeric()):
            HA = HA + float(HB[index])
    if (SA > 0 and HA > 0):
        flagIngresos = True
    else:
        if(SA > 0):
            flagTipoIngreso = True
        else:
            flagTipoIngreso = False
    
    flagResultado = False # True si corresponde pago de impuestos
    flagCaso = 0 # 1 si llena todas las casillas y percibe ambos tipos de ingresos, 2 si llena todas las casillas y sólo percibe ingresos por salarios, 3 si llena todas las casillas y sólo percibe ingresos por honorarios, 4 si no llena todas las casillas y percibe ambos tipos de ingresos, 5 si no llena todas las casillas y sólo percibe ingresos por salarios, 6 si no llena todas las casillas y sólo percibe ingresos por honorarios.
    conectar = connectDB()
    cursor1 = conectar.cursor()

    todays_date = date.today()

    if(anio == todays_date.year):
        cursor1.execute(f""" SELECT porcentaje FROM CM WHERE anio={anio-1}; """)
    elif(anio < todays_date.year):
        cursor1.execute(f""" SELECT porcentaje FROM CM WHERE anio={anio}; """)
    else:
        success_message = 'Error. No se pueden realizar estimaciones de años futuros.'
        flash(success_message)
        return redirect('/')  #error

    cm = cursor1.fetchall()
    CMList = list(cm)
    CM = []
    for index in range(11):
            CM.append(CMList[index][0])

    if(flagProyeccion == False):
        if(flagIngresos):
            flagCaso = 1
            # Salarios:
            # 1. Cálculo de impuestos retenidos anuales
            IRA = 0
            for index in range(11):
                IRA = IRA + (float(IR[index])*(CM[index]/100)) + float(IR[index])

            IRA = IRA + float(IR[11])
        
            # 2. Cálculo de salario imponible anual
            RIA = 0
            for index in range(11):
                RIA = RIA + (float(SI[index])*(CM[index]/100)) + float(SI[index])
            
            RIA = RIA + float(SI[11])

            # Honorarios
            # 1. Cálculo de honorarios retenidos anuales
            HRA = 0
            for index in range(11):
                HRA = HRA + (float(HR[index])*(CM[index]/100)) + float(HR[index])

            HRA = HRA + float(HR[11])
        
            # 2. Cálculo de honorario imponible anual
            HIA = 0
            for index in range(11):
                HIA = HIA + (float(HB[index])*(CM[index]/100)) + float(HB[index])
            
            HIA = HIA + float(HB[11])
            HIA = HIA * 0.7
        
            # Salarios + Honorarios
            # 1. Cálculo de impuesto anual a pagar
            IIA = RIA + HIA # Ingresos imponibles anuales
            cursor2 = conectar.cursor()
            cursor2.execute(f""" SELECT factor FROM IA WHERE desde <= {IIA} AND hasta > {IIA}; """)
            f = cursor2.fetchall()
            F = list(f)
            cursor2.execute(f""" SELECT CR FROM IA WHERE desde <= {IIA} AND hasta > {IIA}; """)
            cr = cursor2.fetchall()
            CR = list(cr)
            IAA = (IIA*F[0][0]) - CR[0][0]

            # 2. Cálculo de impuesto total
            res = IAA - (HRA + IRA)
            
        else:
            if(flagTipoIngreso):
                flagCaso = 2
                # 1. Cálculo de impuestos retenidos anuales
                IRA = 0
                for index in range(11):
                    IRA = IRA + (float(IR[index])*(CM[index]/100)) + float(IR[index])

                IRA = IRA + float(IR[11])

                print(IRA)
                print(CM)
            
                # 2. Cálculo de salario imponible anual
                RIA = 0
                for index in range(11):
                    RIA = RIA + (float(SI[index])*(CM[index]/100)) + float(SI[index])
                
                RIA = RIA + float(SI[11])

                print(RIA)

                # 3. Cálculo de impuesto anual a pagar
                cursor2 = conectar.cursor()
                cursor2.execute(f""" SELECT factor FROM IA WHERE desde <= {RIA} AND hasta > {RIA}; """)
                f = cursor2.fetchall()
                F = list(f)
                cursor2.execute(f""" SELECT CR FROM IA WHERE desde <= {RIA} AND hasta > {RIA}; """)
                cr = cursor2.fetchall()
                CR = list(cr)
                IAA = (RIA*F[0][0]) - CR[0][0]

                # 4. Cálculo de impuesto total
                res = IAA - IRA
                
            else:
                flagCaso = 3
                # 1. Cálculo de honorarios retenidos anuales
                HRA = 0
                for index in range(11):
                    HRA = HRA + (float(HR[index])*(CM[index]/100)) + float(HR[index])
                    
                    print(HRA)

                HRA = HRA + float(HR[11])

                print(HRA)
            
                # 2. Cálculo de honorario imponible anual
                HIA = 0
                for index in range(11):
                    HIA = HIA + (float(HB[index])*(CM[index]/100)) + float(HB[index])
                
                HIA = HIA + float(HB[11])
                HIA = HIA * 0.7

                print(HIA)
            
                # 3. Cálculo de impuesto anual a pagar
                cursor2 = conectar.cursor()
                cursor2.execute(f""" SELECT factor FROM IA WHERE desde <= {HIA} AND hasta > {HIA}; """)
                f = cursor2.fetchall()
                F = list(f)
                cursor2.execute(f""" SELECT CR FROM IA WHERE desde <= {HIA} AND hasta > {HIA}; """)
                cr = cursor2.fetchall()
                CR = list(cr)
                IAA = (HIA*F[0][0]) - CR[0][0]

                print(IAA)
                print(HR)

                # 4. Cálculo de impuesto total de honorarios
                res = IAA - HRA

                

    else: 
        if(flagIngresos):
            flagCaso = 4
            # Salarios:
            # 1. Cálculo de impuestos retenidos anuales
            IRA = 0
            for index in range(mesProyeccion):
                IRA = IRA + (float(IR[index])*(CM[index]/100)) + float(IR[index])

            print('IRA: ', IRA)
            print('correción monetaria: ', CM)

            prom = IRA/(mesProyeccion)
            IRA = IRA + ((12-mesProyeccion)*prom)

            print('IRA + promedios: ', IRA)
            print('promedio:', prom)
            print('mes proyección', mesProyeccion)
            
            # 2. Cálculo de salario imponible anual
            RIA = 0
            for index in range(mesProyeccion):
                RIA = RIA + (float(SI[index])*(CM[index]/100)) + float(SI[index])
            
            print('RIA: ', RIA)
            prom = RIA/(mesProyeccion)
            RIA = RIA + ((12-mesProyeccion)*prom)
            print('promedio RIA:' , prom)

            # Honorarios
            # 1. Cálculo de honorarios retenidos anuales
            HRA = 0
            for index in range(mesProyeccion):
                HRA = HRA + (float(HR[index])*(CM[index]/100)) + float(HR[index])

            prom = HRA/(mesProyeccion)
            HRA = HRA + ((12-mesProyeccion)*prom)

            print('promedio honorario: ', prom)
            print('HRA: ', HRA)

        
            # 2. Cálculo de honorario imponible anual
            HIA = 0
            for index in range(mesProyeccion):
                HIA = HIA + (float(HB[index])*(CM[index]/100)) + float(HB[index])

            prom = HIA/(mesProyeccion)
            HIA = HIA + ((12-mesProyeccion)*prom)
            HIA = HIA * 0.7
        
            # Salarios + Honorarios
            # 1. Cálculo de impuesto anual a pagar
            IIA = RIA + HIA # Ingresos imponibles anuales
            print('IIA: ', IIA)
            cursor2 = conectar.cursor()
            cursor2.execute(f""" SELECT factor FROM IA WHERE desde <= {IIA} AND hasta > {IIA}; """)
            f = cursor2.fetchall()
            F = list(f)
            cursor2.execute(f""" SELECT CR FROM IA WHERE desde <= {IIA} AND hasta > {IIA}; """)
            cr = cursor2.fetchall()
            CR = list(cr)
            IAA = (IIA*F[0][0]) - CR[0][0]

            print('HRA+IRA: ', HRA+IRA)
           

            # 2. Cálculo de impuesto total
            res = IAA - (HRA + IRA)
            
        else:  
            if(flagTipoIngreso):
                flagCaso = 5
                # 1. Cálculo de impuestos retenidos anuales
                IRA = 0
                for index in range(mesProyeccion-1):
                    IRA = IRA + (float(IR[index])*(CM[index]/100)) + float(IR[index])

                prom = IRA/(mesProyeccion)
                IRA = IRA + ((12-mesProyeccion)*prom)
            
                # 2. Cálculo de salario imponible anual
                RIA = 0
                for index in range(mesProyeccion-1):
                    RIA = RIA + (float(SI[index])*(CM[index]/100)) + float(SI[index])
                
                prom = RIA/(mesProyeccion)
                RIA = RIA + ((12-mesProyeccion)*prom)

                # 3. Cálculo de impuesto anual a pagar
                cursor2 = conectar.cursor()
                cursor2.execute(f""" SELECT factor FROM IA WHERE desde <= {RIA} AND hasta > {RIA}; """)
                f = cursor2.fetchall()
                F = list(f)
                cursor2.execute(f""" SELECT CR FROM IA WHERE desde <= {RIA} AND hasta > {RIA}; """)
                cr = cursor2.fetchall()
                CR = list(cr)
                IAA = (RIA*F[0][0]) - CR[0][0]

                # 4. Cálculo de impuesto total
                res = IAA - IRA
            else:
                flagCaso = 6
                # 1. Cálculo de honorarios retenidos anuales
                HRA = 0
                for index in range(mesProyeccion-1):
                    HRA = HRA + (float(HR[index])*(CM[index]/100)) + float(HR[index])

                prom = HRA/(mesProyeccion)
                HRA = HRA + ((12-mesProyeccion)*prom)
            
                # 2. Cálculo de honorario imponible anual
                HIA = 0
                for index in range(mesProyeccion-1):
                    HIA = HIA + (float(HB[index])*(CM[index]/100)) + float(HB[index])

                prom = HIA/(mesProyeccion)
                HIA = HIA + ((12-mesProyeccion)*prom)
                HIA = HIA * 0.7
            
                # 3. Cálculo de impuesto anual a pagar
                cursor2 = conectar.cursor()
                cursor2.execute(f""" SELECT factor FROM IA WHERE desde <= {HIA} AND hasta > {HIA}; """)
                f = cursor2.fetchall()
                F = list(f)
                cursor2.execute(f""" SELECT CR FROM IA WHERE desde <= {HIA} AND hasta > {HIA}; """)
                cr = cursor2.fetchall()
                CR = list(cr)
                IAA = (HIA*F[0][0]) - CR[0][0]

                # 4. Cálculo de impuesto total de honorarios
                res = IAA - HRA
    if(res > 0):
        flagResultado = True
    else:
        flagResultado = False

    return render_template('resultados.html', anio=anio, res = abs(res), caso = flagCaso, pago=flagResultado)

if __name__ == '__main__':
    app.run(debug=True)