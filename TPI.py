class Proceso:
    idproc=int
    Tamaño=int
    TA=int
    TI=int

class CPU:
    proceso= Proceso
    TI_restante=int
    particion = int

proceso_ejecucion = CPU  
proceso_ejecucion.proceso=None 
proceso_ejecucion.TI_restante=None

#--------------------------MEMORIA-------------------------------------
class Particion:
    idpart=int
    dirinicio=int
    T_part=int
    proc= Proceso
    FI=int          #FI = Fragmentacion interna

part1 = Particion()
part2 = Particion()
part3 = Particion()
#Inicializo particion 1
part1.idpart=1
part1.dirinicio=100
part1.T_part=250
part1.proc=None
part1.FI=0
#Inicializo particion 2
part2.idpart=2
part2.dirinicio=350
part2.T_part=120
part2.proc=None
part2.FI=0
#Inicializo particion 3
part3.idpart=3
part3.dirinicio=470
part3.T_part=60
part3.proc=None
part3.FI=0

#Creo la memoria, con 3 particiones
memoria=[part1, part2, part3]

#---------------------------------PROCEDURES-----------------------------------

def carga_procesos():
    bandera = 1
    contador=0
    while bandera == 1:
        Lista_procesos.append(Proceso())
        Lista_procesos[contador].idproc=contador+1
        Lista_procesos[contador].Tamaño= int(input("\n Ingrese el tamaño del proceso: "))
        Lista_procesos[contador].TA = int(input("Ingrese el tiempo de arribo del proceso: "))
        Lista_procesos[contador].TI = int(input("Ingrese el tiempo de irrupcion del proceso: "))
        print("\n")
        contador = contador+1
        if (contador < Max_procesos):
            bandera = int(input("\n ¿Desea ingresar otro proceso? (1=SI | 0=NO): "))
        else:
            print("Has alcanzado el numero máximo de procesos aceptados")
            bandera = 0

def add_cola_espera_memoria():
    global cola_memoria
    for i in range(0, len(Lista_procesos)): 
        if Lista_procesos[i].TA==IT:
            cola_memoria.append(Lista_procesos[i])
            cola_memoria = sorted (cola_memoria, key=lambda x: x.TI) #Ordeno la lista por TI
        i=i+1
            
def comprobar_terminado():
    global CPT
    if proceso_ejecucion.TI_restante==0:
        print("Terminó el proceso: ",proceso_ejecucion.proceso.idproc)   ###SACAAAAAAAAR
        #Libero CPU
        proceso_ejecucion.TI_restante=None
        proceso_ejecucion.proceso=None
        #Libero el espacio de memoria ocupado
        memoria[proceso_ejecucion.particion].proc = None 
        memoria[proceso_ejecucion.particion].FI = 0 
        proceso_ejecucion.particion = None
        CPT=CPT+1 #Incremento en 1 al contador de procesos terminados
        print("\n Memoria")
        print("part / tamaño / proceso/ fragmentacion")
        for i in range(0,len(memoria)):
            if memoria[i].proc==None:
                print(memoria[i].idpart,"\t",memoria[i].T_part,"\t","vacio","\t",memoria[i].FI)
            else:
                 print(memoria[i].idpart,"\t",memoria[i].T_part,"\t",memoria[i].proc.idproc,"\t",memoria[i].FI)
            i=i+1

def cargar_memoria(): #BEST FIT
    pos = 0
    cargados=[]
    carga=0
    for i in range(0, len(cola_memoria)): #Recorro lista de procesos esperando a entrar a memoria
        minfrag = 9999999 #Fragmentacion minima
        for j in range(0, len(memoria)): #recorro las particiones de la memoria
            frag = (memoria[j].T_part - cola_memoria[i].Tamaño) #frag = fragmentacion interna que tendria el proceso si lo cargo en esa particion
            if (frag>=0 and frag<minfrag and memoria[j].proc==None):
                minfrag=frag
                pos=j #Guardo la posicion en la que el proceso generó menos FI
            j=j+1
            
        if pos>=0 and minfrag!=9999999:      
            memoria[pos].proc = cola_memoria[i] #Cargo el proceso en la particion
            memoria[pos].FI = minfrag #Guardo el dato de cuanta fragmentación interna existe con este proceso cargado
            print("Se cargo el proceso: ", memoria[pos].proc.idproc ," en la particion: ", pos+1, "con FragInt = ", memoria[pos].FI)
            cargados.append(cola_memoria[i])
            carga=1
        i=i+1
    if cargados != None:
        for i in range(0,len(cargados)):
            cola_memoria.remove(cargados[i])
            i=i+1
    if carga == 1:
        print("Memoria")
        print("part / tamaño / proceso/ fragmentacion")
        for i in range(0,len(memoria)):
            if memoria[i].proc==None:
                print(memoria[i].idpart,"\t",memoria[i].T_part,"\t","vacio","\t",memoria[i].FI)
            else:
                 print(memoria[i].idpart,"\t",memoria[i].T_part,"\t",memoria[i].proc.idproc,"\t",memoria[i].FI)
            i=i+1
def SJF():
    if proceso_ejecucion.proceso==None:
        Menor= 99999 
        i=0
        proc=None
        part=None
        while i < len(memoria): #Escojo el proceso en memoria con menor TI
            if ((memoria[i].proc != None) and (memoria[i].proc.TI < Menor)): #Si la posicion de memoria en donde estoy no esta vacia AND el TI<Menor
                Menor=memoria[i].proc.TI #Guardo el menor TI
                proc=memoria[i].proc #Guardo el proceso en una variable para su posterior asignacion al procesador
                part = i #Guardo la ubicacion del proceso con TI mas corto (esto va a servir en un futuro cuando quiera liberar la CPU del proceso que esta corriendo)
            i=i+1
        #Cargo el proceso con menor TI en la CPU
        proceso_ejecucion.proceso = proc
        proceso_ejecucion.TI_restante = Menor
        proceso_ejecucion.particion = part

#---------------------Inicializo variables--------------------------------
Lista_procesos=[]
Max_procesos = 10 #Por consigna el tamaño maximo de procesos será 10
cola_memoria = []
#----------------------------------------------EJECUCION-------------------------------------------
CPT = 0 #CPT = contador de procesos terminados
IT = 0 #IT = Instante de tiempo (actual)
carga_procesos()

while CPT < len(Lista_procesos): #Mientras la cantidad de procesos terminados sea menor que la cantidad de procesos cargados continuará en while
    print("\n  \t \t \t \t INSTANTE ", IT,"\n")
    if proceso_ejecucion.proceso != None : #Si hay un proceso en CPU le descuento un tiempo de interrupcion
        proceso_ejecucion.TI_restante=proceso_ejecucion.TI_restante-1
    add_cola_espera_memoria()
    comprobar_terminado()
    cargar_memoria()
    SJF()
    if proceso_ejecucion.proceso != None :
        print ("--> Proceso en ejecución: ", (proceso_ejecucion.proceso).idproc)
    IT=IT+1
    input("\n\n ------------------------------------------------------------------ENTER to continue")


input("\n\n ------------------------------------------------------------------ENTER to finish") ###SACAR

#FALTA ::: Una vez que un proceso que estaba en cola_memoria se carga a la memoria, hay que sacarlo de esa cola