import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re

print('Para facilitar el analísis estadístico de lo acontecido en el Titanic, se realizó este programa: permite seleccionar, de una lista, un gráfico a generar en función de las variables existentes y pertinentes a dicho tipo de gráfico.')

                                            # PREPARAMOS EL DATAFRAME

# Abrimos el archivo
df = pd.read_csv('Titanic.csv', encoding='UTF-8', sep=',')
# Eliminamos las columnas "PassengerId", "Ticket" y "Cabin" porque no las usaremos
df = df.drop(["PassengerId", "Ticket", "Cabin"], axis=1)
# Y queremos que los nombres estén por delante de todo a cambio del ID
new_order = ['Name', 'Survived', 'Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
df = df[new_order]
# Reemplazamos los valores en la columna "Sex" por "femenino" y "masculino", y los 1 y 0 de "Supervivencia" por "Sí" y "No"
df['Sex'] = df['Sex'].replace({'female': 'femenino', 'male': 'masculino'})
df['Survived'] = df['Survived'].replace({1: 'Sí', 0: 'No'})
# Renombramos las columnas en español
espanol = {
    'Name': 'Nombre',
    'Survived': 'Supervivencia',
    'Pclass': 'Clase',
    'Sex': 'Género',
    'Age': 'Edad',
    'SibSp': 'N_hermanos_cónyuge',
    'Parch': 'N_padres_hijos',
    'Fare': 'Tarifa',
    'Embarked': 'Embarque'
}
df = df.rename(columns=espanol)

print('Previsualización del dataset:')
print(df.head(10))
print(df.tail(10))


                                            # FUNCIONES

# Funciones para los gráficos de matplot.lib que se le ofrecerán al usuario en el menú

def frecuencia (variable): # Variables pertinentes: Edad, N_hermanos_cónyuge, N_padres_hijos
    plt.hist(df[variable].dropna(), bins=20, color='skyblue')
    plt.xlabel(variable)
    plt.ylabel('Frecuencia')
    plt.title('Distribución de ' + variable + ' de los Pasajeros')
    plt.show()

def grafico_torta(variable): # Variables pertinentes: Supervivencia, Clase, Sexo, Embarque
    cat_counts = df[variable].value_counts()
    plt.pie(cat_counts, labels=cat_counts.index, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Distribución de ' + variable + ' de los Pasajeros')
    plt.show()

def promedio(variable): # Variables pertinentes: Tarifa x Clase o Género o Embarque
    promedio_r1_r2 = df.groupby(variable)['Tarifa'].mean()
    promedio_r1_r2.plot(kind='bar')
    plt.xlabel(variable)
    plt.ylabel('Tarifa')
    plt.title('Promedio de Tarifa por ' + variable)
    plt.show()

def diferencia(categoria, a_diferenciar): # Variables pertinentes: Clase x Supervivencia o Género, Embarque x Supervivencia o Género
    survival_by_class = df.groupby(categoria)[a_diferenciar].value_counts().unstack()
    survival_by_class.plot(kind='bar', stacked=True)
    plt.xlabel(categoria)
    plt.ylabel('Cantidad')
    plt.title(a_diferenciar + ' por ' + categoria)
    plt.legend(title=a_diferenciar, labels=['No', 'Sí'])
    plt.show()


# Funciones para los GRAFOS de NetworkX basados en la búsqueda de la expresión literal: apellido, que encuentra a todos los
# pasajeros con dicho apellido y los relaciona con la variable elegida de las tres dadas: género, clase o supervivencia

def validar_busqueda(apellido,data_a_validar):
    #Si está vacío, arrojará un excepción. 
    if data_a_validar.empty:
            raise ValueError(f"No se encontraron registros para el apellido {apellido} proporcionado")

def retornar_categoria_elegida(opcion):
    opciones_disponibles = {1:["Género",["masculino", "femenino"]],
                            2:["Clase",[1, 2, 3]],
                            3:["Supervivencia",["Sí", "No"]]
                        }
    
    if opcion in opciones_disponibles.keys():
        return opciones_disponibles[opcion]
    raise ValueError(f"No se encontró la opción{opcion}, intente con un valor válido tales como: {opciones_disponibles.keys()}")
    
def generar_grafo_por_categoria(apellido, data, opcion):
    try:
        #Expresiones regulares para obtener el apellido de las columna Name.
        apellido = "^" + re.escape(apellido.capitalize()) + ".*"
        
        #Filtrar el DataFrame para incluir solo las filas que coinciden con el nombre dado
        data_filtrada = data[data['Nombre'].str.match(apellido)]

        #validar la busqueda
        validar_busqueda(apellido,data_filtrada)
        
        #validar_opcion. Retorna la categoria a buscar.(unpacking)
        categoria, valores_categoria = retornar_categoria_elegida(opcion)
        
        #Crear un grafo dirigido
        DG = nx.DiGraph()
        
        #Agregar nodos y bordes al grafo
        for i in range(0, len(data_filtrada)):
            DG.add_edge(data_filtrada.iloc[i]['Nombre'], data_filtrada.iloc[i][categoria])
        
        #Definir colores para los nodos
        
        color_nodos = ['red' if node in valores_categoria else 'lightblue' for node in DG.nodes()]
        
        #Dibujar grafo
        fig, ax = plt.subplots(figsize = (20,20))
        
        nx.draw(DG, with_labels=True, node_size = 1500,node_color= color_nodos)
        plt.show()
    
    except Exception as e:
        print(f"Error:{e}")

def por_multifuncion(apellido, Data):

    apellido = "^" + re.escape(apellido.capitalize()) + ".*"
    data_filtrada = Data[Data['Nombre'].str.match(apellido)]
    validar_busqueda(apellido,data_filtrada)

    fig, ax = plt.subplots(figsize =(12,12))

    opciones = input("Seleccione la o las variables que desea incluir (escriba cada número separado por un espacio):\n1. Por género\n2. Por clase\n3. Por supervivencia")
    

    DG = nx.DiGraph()
    for i in range(0, len(data_filtrada)):
        if re.search("1", opciones):
            DG.add_edge(data_filtrada.iloc[i]['Nombre'], data_filtrada.iloc[i]['Género'])
        if re.search("2", opciones): 
            DG.add_edge(data_filtrada.iloc[i]['Nombre'], data_filtrada.iloc[i]['Clase'])
        if re.search("3", opciones):  
            DG.add_edge(data_filtrada.iloc[i]['Nombre'], data_filtrada.iloc[i]['Supervivencia'])
        i = i + 1 
    d = dict(DG.degree)
    clase = [1, 2, 3]
    genero = ["masculino", "femenino"]
    supervivencia = ["Sí", "No"]
    pos = nx.spring_layout(DG, k=3, scale=2.0)
    nx.draw(DG,pos, with_labels=True, node_color= ['red' if node in supervivencia else 'green' if node in clase else 'yellow' if node in genero else 'lightblue' for node in DG.nodes()])
    plt.show()
                                            # MENÚ DE USO

# Para el usuario

acceso_menu = True
while acceso_menu:
    menu_principal = int(input('Ingrese el número de la opción del menú que desee elegir:\n1. Generar un gráfico de frecuencia\n2. Generar un gráfico de torta\n3. Generar un promedio de la Tarifa por una variable\n4. Generar una diferencia \n5. Generar un grafo en base a un apellido\n0. SALIR'))

    if(menu_principal == 1): # Submenú Frecuencia
        variable = int(input('Frecuencia que desea generar:\n1. Edad\n2. Hermanos/cónyuges\n3. Padres/hijos'))
        if(variable == 1):
            frecuencia('Edad')
        elif(variable == 2):
            frecuencia("N_hermanos_cónyuge")
        elif(variable == 3):
            frecuencia("N_padres_hijos")
        else: print('Esa opción no existe')
    elif(menu_principal == 2): # Submenú Torta
        variable = int(input('Sobre qué desea hacer el gráfico de torta:\n1. Supervivientes\n2. Clase\n3. Género\n4. Embarque'))
        if(variable == 1):
            grafico_torta('Supervivencia')
        elif(variable == 2):
            grafico_torta("Clase")
        elif(variable == 3):
            grafico_torta("Género")
        elif(variable == 4):
            grafico_torta('Embarque')
        else: print('Esa opción no existe')
    elif(menu_principal == 3): # Submenú Promedio
        variable = int(input('Calcule el promedio de la TARIFA por una variable:\n1. Clase\n2. Género\n3. Embarque'))
        if(variable == 1):
            promedio('Clase')
        elif(variable == 2):
            promedio("Género")
        elif(variable == 3):
            promedio("Embarque")
        else: print('Esa opción no existe')
    elif(menu_principal == 4): # Submenú Diferencia
        variable1 = int(input('Categoría dentro de la cual diferenciar:\n1. Clase\n2. Embarque'))
        if(variable1 == 1):
            variable1 = 'Clase'
            variable2 = int(input('1. Supervivencia\n2. Género\nVariable a diferenciar:'))
            if(variable2 == 1):
                variable2 = 'Supervivencia'
                diferencia(variable1, variable2)
            elif(variable2 == 2):
                variable2 = 'Género'
                diferencia(variable1, variable2)
            else: print('Esa opción no existe')
        elif(variable1 == 2):
            variable1 = 'Embarque'
            variable2 = int(input('1. Supervivencia\n2. Género\nVariable a diferenciar:'))
            if(variable2 == 1):
                variable2 = 'Supervivencia'
                diferencia(variable1, variable2)
            elif(variable2 == 2):
                variable2 = 'Género'
                diferencia(variable1, variable2)
            else: print('Esa opción no existe')
        else: print('Esa opción no existe')
    elif(menu_principal == 5): # Submenú GRAFOS 
        menu_acceso = True
        while menu_acceso:
            Data = pd.read_csv('Titanic.csv')
            apellido = input('Ingrese el apellido que desea buscar:')

            menu = int(input('Elija el parámetro de búsqueda (número de la opción):\n1. Por género\n2. Por clase\n3. Por supervivencia\n4. Por multifuncion\n5. Reiniciar la búsqueda\n0. SALIR'))

            if(menu == 1):
                generar_grafo_por_categoria(apellido, df, 1)
            elif(menu == 2):
                generar_grafo_por_categoria(apellido, df, 2)
            elif(menu == 3):
                generar_grafo_por_categoria(apellido, df, 3)
            elif(menu == 4):
                por_multifuncion(apellido, df)
            elif(menu == 5):
                print('Reiniciando búsqueda')
                menu_acceso = True
            elif(menu == 0):
                menu_acceso = False
            else: print('Esa opción no existe. Reiniciando búsqueda...')
    elif(menu_principal == 0): # SALIR
        acceso_menu = False
    else: acceso_menu = True