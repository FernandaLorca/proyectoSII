from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import psycopg2.extras
import os


app = Flask(__name__)

def connectDB():
    connectionString='dbname=taxhelp user=rafa password=delunoaldiez host=localhost' # se definen los parámetros para establecer la conexión a la base de datos local taxhelp
    print(connectionString) 
    try:
        return psycopg2.connect(connectionString) # se lanza un try para establecer la conexión
    except:
        print("No se pudo conectar.") # se imprime este mensaje en caso de no conseguir establecer la conexión

@app.route('/') # se define el procedimiento cuando la ruta es /
def index(): # se define la función index()

    conectar = connectDB() 
    cursor=conectar.cursor() 
    cursor.execute("""SELECT distinct anio FROM IA;""") # se ejecuta la consulta sql 
        
    anios=cursor.fetchall() # se almacena el resultado de dicha consulta en el cursor anios

    return render_template('index.html', anios=anios) # se define el retorno de la función: redireccionar al template index.html entregando el parámetro anios que corresponde al cursor del mismo nombre, definido antes

@app.route('/calculo/<int:anio>') # se define el procedimiento cuando la ruta es /calculo/<int:anio>
def calculo(anio): # se define la función calculo(anio) donde el argumento es aquel entero anio presente en la ruta

    conectar = connectDB()
    cursor=conectar.cursor()
    cursor.execute(f"""SELECT * FROM IA WHERE anio={anio};""") # se ejecuta la consulta sql que retorna todas las tuplas de la tabla IA (impuesto anual) donde anio=anio
        
    ans=cursor.fetchall() # se almacena el resultado de dicha consulta en el cursor ans
   
    return render_template('calculo.html', ans=ans) # se define el retorno de la función: redireccionar al template calculo.html entregando el parámetro ans que corresponde al cursor del mismo nombre, definido antes

@app.route('/admin', methods=['GET', 'POST']) # se define el procedimiento cuando la ruta es /admin, también se consideran los métodos GET y POST
def admin(): # se define la función admin()
    if request.method=='GET':
        return render_template('adminlogin.html') # se establece que, cuando se intenta ejecutar un requerimiento GET, se redireccionará al template adminlogin.html
    else:
        user = request.form.get("password") # se define la variable user que almacenará el valor del form password, que se entrega a través del método POST

        if user=='sii123': # si user es correcto

            conectar = connectDB()
            cursor=conectar.cursor()
            cursor.execute("""SELECT desde, hasta, factor, CR, anio
                            FROM IA order by anio, factor; """) # se ejecuta la consulta sql que retorna todas las tuplas de la tabla IA (impuesto anual) ordenadas por anio y factor
        
            datos=cursor.fetchall() # se almacena el resultado de dicha consulta en el cursor datos

            conectar = connectDB()
            cursor=conectar.cursor()
            cursor.execute("""SELECT mes, porcentaje, anio
                            FROM CM order by anio; """) # se ejecuta la consulta sql que retorna todas las tuplas de la tabla CM (corrección monetaria) ordenadas por anio

            cm=cursor.fetchall() # se almacena el resultado de dicha consulta en el cursor cm

            ctx = {
            "datos" : datos,
            "cm" : cm
            } # se define la variable ctx que almacena los dos cursores definidos anteriormente
            
            return render_template('admin.html', contexto=ctx) # se define el retorno de la función: redireccionar al template admin.html entregando el parámetro contexto que corresponde al cursor ctx, definido antes

        else: # si user no es correcto
             return render_template('index.html') # se redirecciona al template index.html

@app.route('/ingresarcm', methods=['GET', 'POST']) # se define el procedimiento cuando la ruta es /ingresarcm, también se consideran los métodos GET y POST
def ingresarcm(): # se define la función ingresarcm()

    if request.method=='GET':
        return render_template('ingresarcm.html') # se establece que, cuando se intenta ejecutar un requerimiento GET, se redireccionará al template ingresarcm.html

    else:
        # se definen las variable mes, porcentaje y anio que almacenarán los valores de los form mes, porcentaje y anio, que se entregarán a través del método POST
        mes = request.form.get("mes") 
        porcentaje = request.form.get("porcentaje")
        anio = request.form.get("anio")

        sql = 'INSERT INTO CM (mes, porcentaje, anio) VALUES(%s,%s,%s)' # se define la variable sql para el ingreso de datos a la tabla CM (corrección monetaria)

        datos = (mes, porcentaje, anio) # se define la variable datos que alberga los parámetros de la sentencia INSERT

        conectar = connectDB()
        cursor=conectar.cursor()

        print(sql) # se imprime la sentencia

        try:
            cursor.execute(sql,datos)
            conectar.commit() # se ejecuta el ingreso de datos dentro de un statement try
            return render_template('ingresarcm.html') # se redirecciona al template ingresarcm.html en caso de conseguir ingresar los datos
        except:
            return render_template('ingresarcm.html') # se redirecciona al template ingresarcm.html en caso de no conseguir ingresar los datos
    

@app.route('/ingresaria', methods=['GET', 'POST']) # se define el procedimiento cuando la ruta es /ingresaria, también se consideran los métodos GET y POST
def ingresaria(): # se define la función ingresaria()

    if request.method=='GET':
        return render_template('ingresaria.html') # se establece que, cuando se intenta ejecutar un requerimiento GET, se redireccionará al template ingresaria.html

    else:
        # se definen las variables desdeIA, hastaIA, factorIA, cr y anio que almacenarán los valores de los form desdeIA, hastaIA, factorIA, CR y anio que se entregarán a través del método POST
        desdeIA = request.form.get("desdeIA")
        hastaIA = request.form.get("hastaIA")
        factorIA = request.form.get("factorIA")
        cr = request.form.get("CR")
        anio = request.form.get("anio")

        sql = 'INSERT INTO IA (desde, hasta, factor, CR, anio) VALUES(%s,%s,%s,%s,%s)' # se define la variable sql para el ingreso de datos a la tabla IA (impuesto anual)

        datos = (desdeIA, hastaIA, factorIA, cr, anio) # se define la variable datos que alberga los parámetros de la sentencia INSERT

        conectar = connectDB()
        cursor=conectar.cursor()

        cursor.execute(sql, datos) 

        conectar.commit() # se ejecuta el ingreso de datos
    
    return render_template('ingresaria.html') # se redirecciona al template ingresaria.html

@app.route('/eliminaria', methods=['GET', 'POST']) # se define el procedimiento cuando la ruta es /eliminaria, también se consideran los métodos GET y POST
def eliminaria(): # se define la función eliminaria()

    conectar = connectDB()
    cursor=conectar.cursor()
    cursor.execute("""SELECT desde, hasta, factor, CR, anio
                            FROM IA order by anio, factor; """) # se ejecuta la consulta sql que retorna todas las tuplas de la tabla IA (impuesto anual) ordenadas por anio y factor
        
    datos=cursor.fetchall()  # se almacena el resultado de dicha consulta en el cursor datos

    conectar = connectDB()
    cursor=conectar.cursor()
    cursor.execute("""SELECT mes, porcentaje, anio
                       FROM CM order by anio; """) # se ejecuta la consulta sql que retorna todas las tuplas de la tabla CM (corrección monetaria) ordenadas por anio

    cm=cursor.fetchall() # se almacena el resultado de dicha consulta en el cursor cm

    ctx = {
        "datos" : datos,
        "cm" : cm
            } # se define la variable ctx que almacena los dos cursores definidos anteriormente

    if request.method=='GET':
        return render_template('eliminaria.html', contexto=ctx) # se establece que, cuando se intenta ejecutar un requerimiento GET, se redireccionará al template eliminaria.html entregando el parámetro contexto que corresponde al cursor ctx, definido antes

    else:

        # se definen las variables desdeIA, hastaIA, factorIA, cr y anio que almacenarán los valores de los form desdeIA, hastaIA, factorIA, CR y anio que se entregarán a través del método POST
        desdeIA = request.form.get("desdeIA")
        hastaIA = request.form.get("hastaIA")
        factorIA = request.form.get("factorIA")
        cr = request.form.get("CR")
        anio = request.form.get("anio")

        sql = 'DELETE FROM IA WHERE desde=%s AND hasta=%s AND factor=%s AND CR=%s AND anio=%s' # se define la variable sql para la eliminación de datos de la tabla IA (impuesto anual)

        datos = (desdeIA, hastaIA, factorIA, cr, anio) # se define la variable datos que alberga los parámetros de la sentencia DELETE

        conectar = connectDB()
        cursor=conectar.cursor()

        print(sql) # se imprime la sentencia

        cursor.execute(sql,datos)
        conectar.commit() # se ejecuta la eliminación de datos
        return render_template('admin.html', contexto=ctx) # se redirecciona al template admin.html entregando el parámetro contexto que corresponde al cursor ctx, definido antes
        


@app.route('/eliminarcm', methods=['GET', 'POST']) # se define el procedimiento cuando la ruta es /eliminarcm, también se consideran los métodos GET y POST
def eliminarcm():  # se define la función eliminarcm()

    conectar = connectDB()
    cursor=conectar.cursor()
    cursor.execute("""SELECT desde, hasta, factor, CR, anio
                            FROM IA order by anio, factor; """) # se ejecuta la consulta sql que retorna todas las tuplas de la tabla IA (impuesto anual) ordenadas por anio y factor
        
    datos=cursor.fetchall() # se almacena el resultado de dicha consulta en el cursor datos

    conectar = connectDB()
    cursor=conectar.cursor()
    cursor.execute("""SELECT mes, porcentaje, anio
                       FROM CM order by anio; """) # se ejecuta la consulta sql que retorna todas las tuplas de la tabla CM (corrección monetaria) ordenadas por anio

    cm=cursor.fetchall() # se almacena el resultado de dicha consulta en el cursor cm

    ctx = {
        "datos" : datos,
        "cm" : cm
            } # se define la variable ctx que almacena los dos cursores definidos anteriormente

    if request.method=='GET':
        return render_template('eliminarcm.html', contexto=ctx) # se establece que, cuando se intenta ejecutar un requerimiento GET, se redireccionará al template eliminarcm.html entregando el parámetro contexto que corresponde al cursor ctx, definido antes

    else:

        # se definen las variables mes, porcentaje y anio que almacenarán los valores de los form mes, porcentaje y anio que se entregarán a través del método POST
        mes = request.form.get("mes")
        porcentaje = request.form.get("porcentaje")
        anio = request.form.get("anio")

        sql = 'DELETE FROM CM WHERE mes=%s AND porcentaje=%s AND anio=%s' # se define la variable sql para la eliminación de datos de la tabla CM (correción monetaria)

        datos = (mes, porcentaje, anio) # se define la variable datos que alberga los parámetros de la sentencia DELETE

        conectar = connectDB()
        cursor=conectar.cursor()

        print(sql) # se imprime la sentencia

        try:
            cursor.execute(sql,datos)
            conectar.commit() # se ejecuta la eliminación de datos
            return render_template('admin.html', contexto=ctx) # se redirecciona al template admin.html entregando el parámetro contexto que corresponde al cursor ctx, definido antes
        except:
            return render_template('admin.html', contexto=ctx) # se redirecciona al template admin.html entregando el parámetro contexto que corresponde al cursor ctx, definido antes

@app.route('/calcular/<int:anio>',  methods=['POST']) # se define el procedimiento cuando la ruta es /calcular, se considera el método POST
def calcular(anio): # se define la función calcular(anio) que recibe como parámetro el anio a considerar

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
    
    ########## CÁLCULOS ##########

    flagCasillas = False # True si llena todas las casillas
    flagIngresos = False # True si percibe los dos tipos de ingresos
    flagTipoIngreso = False # True si el tipo de ingreso es salario

    flagResultado = False # True si corresponde pago de impuestos
    flagCaso = 0 # 1 si llena todas las casillas y percibe ambos tipos de ingresos, 2 si llena todas las casillas y sólo percibe ingresos por salarios, 3 si llena todas las casillas y sólo percibe ingresos por honorarios, 4 si no llena todas las casillas y percibe ambos tipos de ingresos, 5 si no llena todas las casillas y sólo percibe ingresos por salarios, 6 si no llena todas las casillas y sólo percibe ingresos por honorarios.
    
    if(flagCasillas):
        if(flagIngresos):
            flagCaso = 1
        # Salarios:
        # 1. Cálculo de impuestos retenidos anuales
            IR = [IREnero, IRFebrero, IRMarzo, IRAbril, IRMayo, IRJunio, IRJulio, IRAgosto, IRSeptiembre, IROctubre, IRNoviembre, IRDiciembre] # arreglo de impuestos retenidos por cada mes (de enero a diciembre)
            IRA = 0
            for index in range(10):
                IRA = IRA + (float(IR[index])*CM[index])

            IRA = IRA + float(IR[11])
        
        # 2. Cálculo de salario imponible anual
            SI = [SIEnero, SIFebrero, SIMarzo, SIAbril, SIMayo, SIJunio, SIJulio, SIAgosto, SISeptiembre, SIOctubre, SINoviembre, SIDiciembre] # arreglo de salarios imponibles por cada mes (de enero a diciembre)
            RIA = 0
            for index in range(10):
                RIA = RIA + (float(SI[index])*CM[index])
            
            RIA = RIA + float(SI[11])

        # Honorarios
        # 1. Cálculo de honorarios retenidos anuales
            HR = [HREnero, HRFebrero, HRMarzo, HRAbril, HRMayo, HRJunio, HRJulio, HRAgosto, HRSeptiembre, HROctubre, HRNoviembre,  HRDiciembre] # arreglo de honorarios retenidos por cada mes (de enero a diciembre)
            HRA = 0
            for index in range(10):
                HRA = HRA + (float(HR[index])*CM[index])

            HRA = HRA + float(HR[11])
        
        # 2. Cálculo de honorario imponible anual
            HB = [HBEnero, HBFebrero, HBMarzo, HBAbril, HBMayo, HBJunio, HBJulio, HBAgosto, HBSeptiembre, HBOctubre, HBNoviembre, HBDiciembre] # arreglo de salarios imponibles por cada mes (de enero a diciembre)
            HIA = 0
            for index in range(10):
                HIA = HIA + (float(HB[index])*CM[index])
            
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
            if(res > 0):
                flagResultado = True
            else:
                flagResultado = False

            return render_template('calcular.html', res = abs(res), caso = flagCaso, pago=flagResultado)

        else:
            if(flagTipoIngreso):
                flagCaso = 2
                

            else:

    else: 
        if(flagIngresos):
             
        else:  
            if(flagTipoIngreso):

            else:

    conectar = connectDB()
    cursor1 = conectar.cursor()
    cursor1.execute(""" SELECT porcentaje FROM CM WHERE anio=2021; """)

    cm = cursor1.fetchall()
    CMList = list(cm)
    CM = []
    for index in range(10):
            CM.append(CMList[index][0])
 
    if anio==2021:
        #Salarios:

        # 1. Cálculo de impuestos retenidos anuales
            IR = [IREnero, IRFebrero, IRMarzo, IRAbril, IRMayo, IRJunio, IRJulio, IRAgosto, IRSeptiembre, IROctubre, IRNoviembre, IRDiciembre] # arreglo de impuestos retenidos por cada mes (de enero a diciembre)
            IRA = 0
            for index in range(10):
                IRA = IRA + (float(IR[index])*CM[index])

            IRA = IRA + float(IR[11])
        
        # 2. Cálculo de salario imponible anual
            SI = [SIEnero, SIFebrero, SIMarzo, SIAbril, SIMayo, SIJunio, SIJulio, SIAgosto, SISeptiembre, SIOctubre, SINoviembre, SIDiciembre] # arreglo de salarios imponibles por cada mes (de enero a diciembre)
            RIA = 0
            for index in range(10):
                RIA = RIA + (float(SI[index])*CM[index])
            
            RIA = RIA + float(SI[11])
        
        # 3. Cálculo de impuesto anual a pagar
            cursor2 = conectar.cursor()
            cursor2.execute(f""" SELECT factor FROM IA WHERE desde <= {RIA} AND hasta > {RIA}; """)
            f = cursor2.fetchall()
            F = list(f)
            cursor2.execute(f""" SELECT CR FROM IA WHERE desde <= {RIA} AND hasta > {RIA}; """)
            cr = cursor2.fetchall()
            CR = list(cr)
            IAA = (RIA*F[0][0]) - CR[0][0]

        # 4. Cálculo de impuesto total de salarios
            ITS = IAA - IRA

        #Honorarios

        # 1. Cálculo de honorarios retenidos anuales
            HR = [HREnero, HRFebrero, HRMarzo, HRAbril, HRMayo, HRJunio, HRJulio, HRAgosto, HRSeptiembre, HROctubre, HRNoviembre,  HRDiciembre] # arreglo de honorarios retenidos por cada mes (de enero a diciembre)
            HRA = 0
            for index in range(10):
                HRA = HRA + (float(HR[index])*CM[index])

            HRA = HRA + float(HR[11])
        
        # 2. Cálculo de honorario imponible anual
            HB = [HBEnero, HBFebrero, HBMarzo, HBAbril, HBMayo, HBJunio, HBJulio, HBAgosto, HBSeptiembre, HBOctubre, HBNoviembre, HBDiciembre] # arreglo de salarios imponibles por cada mes (de enero a diciembre)
            HIA = 0
            for index in range(10):
                HIA = HIA + (float(HB[index])*CM[index])
            
            HIA = HIA + float(HB[11])
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
            ITH = IAA - HRA
   
            return render_template('calcular.html', impuestoTotalSalario=ITS, impuestoTotalHonorario=ITH)
    
    return render_template('calcular.html', anio=anio , cm = CM, f = F)

  

if __name__ == '__main__':
    app.run(debug=True)
