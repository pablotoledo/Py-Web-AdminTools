# -*- coding: utf-8 -*-
'''
    FTPy
    # Copyright 2014 Pablo Toledo.
    #
    # Licensed under the Apache License, Version 2.0 (the "License");
    # you may not use this file except in compliance with the License.
    # You may obtain a copy of the License at
    #
    #      http://www.apache.org/licenses/LICENSE-2.0
    #
    # Unless required by applicable law or agreed to in writing, software
    # distributed under the License is distributed on an "AS IS" BASIS,
    # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    # See the License for the specific language governing permissions and
    # limitations under the License.
    
    @author: juanpablotoledogavagnin
    
'''
from ftplib import FTP
import os

#Variables Globales de configuracion
HOST = 'ftp.demisitio.com'
PUERTO = 21
USUARIO = 'usuario'
CLAVE = 'contraseña'
ruta = "/"
destino = "/home/Usuario/Backup" #Especificar la ruta donde queremos que se almacene la copia de seguridad
ftp = FTP()

#Variables globales para logs
listaErrores = []
numErrores = 0

#Metodos
##################################################################
#Metodo de conexion al servidor FTP
def conectar():
    ftp.connect(HOST, PUERTO)
    ftp.login(USUARIO, CLAVE)
    print('Conectado al servidor')
    print(str(ftp.welcome))
    return

#Método recursivo de descarga
def descargaRecursiva(ruta):
    global numErrores
    #Nos movemos a la ruta en el servidor
    ftp.cwd(ruta)
    print('En ruta: '+ruta)
    #Obtenemos una lista de string, cada string define un archivo
    listaInicial =[]
    ftp.dir(listaInicial.append)
    '''
        con dir() obtenemos un string que lista todos los elementos contenido en la ruta
        la estructura obtenida en mi caso fue
        
        drwxr-xr-x    2 362309906  usuario1       4096 Nov  2 15:09 .
        drwxr-x--x    4 362309906  usuario1        4096 Jun  9 08:26 ..
        -rw-r--r--    1 362309906  usuario1         563 Nov  1 17:10 index.html
        
        donde las carpetas comienzan con d y el nombre del archivo/carpeta se ubica al fin
        el string anterior se trata de la siguiente manera:
        -se divide el string en una lista de strings donde cada posición representa una linea
        -cada posición de la lista se subdivide tomando como referencia los espacios formando un
        array bidimensional donde tenemos la información separada y podemos consultarla con más facilidad
        En este caso el array bidimensional tiene en las posiciones:
        -nx0: la información relativa a si es un directorio (d) o un archivo (-) y sus pemisos
        -nx8: el nombre de fichero
        '''
    listaIntermedia = []
    for elemento in listaInicial:
        listaIntermedia.append(str(elemento).split())
    '''
        Tras obtener en listaIntermedia el array bidimensional, generamos dos listas:
        -Una lista de pos[8] (nombres de ficheros) que cumplen que pos[0] no comienza con d
        -Una lista de pos[8] (carpetas) que cumplen que pos[0] comienza con d
        '''
    listaArchivos = []
    listaCarpetas=[]
    for elemento in listaIntermedia:
        if elemento[0].startswith('d'):
            listaCarpetas.append(str(elemento[8]))
        else:
            listaArchivos.append(str(elemento[8]))
    '''
        Eliminamos de la lista de carpetas . y .. para evitar bucles por el servidor
        '''
try:
    listaCarpetas.remove('.')
        listaCarpetas.remove('..')
    except:
        pass
'''
    Listamos los elementos a trabajar de la ruta actual
    '''
        print('\tLista de Archivos: '+str(listaArchivos))
            print('\tLista de Carpetas: '+str(listaCarpetas))

'''
    Si la ruta actual no tiene su equivalente local, creamos la carpeta a nivel local
    '''
        if not os.path.exists(destino+ruta):
        os.makedirs(destino+ruta)
            '''
                Los elementos de la lista de archivo se proceden a descargar de forma secuencial en la ruta
                '''
for elemento in listaArchivos:
    print('\t\tDescargando '+elemento+' en '+destino+ruta)
        try:
            ftp.retrbinary("RETR "+elemento, open(os.path.join(destino+ruta,elemento),"wb").write)
    except:
        print('Error al descargar '+elemento+' ubicado en '+destino+ruta)
            listaErrores.append('Archivo '+elemento+' ubicado en '+destino+ruta)
            numErrores = numErrores+1
'''
    Una vez se termina de descargar los archivos invocamos el método actual provocando una solución
    recursiva, para ello concatenamos la ruta actual con el nombre de la carpeta, realizando tantas
    llamadas al método actual como elementos tengamos listados en listaCarpetas
    '''
        for elemento in listaCarpetas:
        descargaRecursiva(ruta+elemento+'/')
            return

#Método para imprimir resultado de errores detectados y crear un log con los ficheros que dieron fallo
def mostrarLog():
    global numErrores
    print('##################################################################')
    log = open(destino+"/logFTP.txt",'w')
    print('Errores detectados = '+str(numErrores))
    log.write('Errores detectados = '+str(numErrores))
    for elemento in listaErrores:
        log.write('\t'+str(elemento))
        print('\t'+str(elemento))
    print('##################################################################')

#Main
print('Comienza la ejecucion del backup de sitio web '+HOST)
conectar()
descargaRecursiva(ruta)
mostrarLog()
#Desconectamos con el servidor de forma protocolaria
ftp.quit()
print('Conexion cerrada correctamente')
