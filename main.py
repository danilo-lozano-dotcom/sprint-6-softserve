from datetime import datetime # Importación del módulo datetime para manejar fechas
import logging # Importación del módulo logging para manejar registros de eventos
import csv # Importación del módulo csv para manejar archivos CSV
import json # Importación del módulo json para manejar archivos JSON
import os # Importación del módulo os para manejar operaciones del sistema operativo

# Archivos donde se alamcenrán los datos de las mascotas y sus consultas
archivo_csv = 'mascotas_dueños.csv'
archivo_json = 'consultas.json'



# Implementación de la configuración del sistema de logging para registrar eventos y errores
logging.basicConfig(
    filename='clinica_veterinaria.log', # Archivo donde se guardarán los logs
    level=logging.INFO, # Nivel de logging INFO para registrar eventos informativos
    format='%(asctime)s - %(levelname)s - %(message)s') # Formato de los mensajes de los evventos o logs


# Definición de la clase Dueño que almacena información del dueño de la mascota
class Dueno:
    def __init__(self, nombre, telefono, direccion):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion

    # Método para mostrar la información del dueño
    def __str__(self):
        return f"Dueño: {self.nombre}, Teléfono: {self.telefono}, Dirección: {self.direccion}"


# Definición de la clase Mascota que almacena información de la mascota y su dueño
class Mascota:
    def __init__(self, nombre, especie, raza, edad, dueno):
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.edad = edad
        self.dueno = dueno
        self.consultas = []

    def agregar_consulta(self, consulta):
        self.consultas.append(consulta)

    # Método para mostrar la información de la mascota y su dueño
    def __str__(self):
        return (f"Nombre: {self.nombre}, Especie: {self.especie}, Raza: {self.raza}, "
                f"Edad: {self.edad}, {self.dueno}")


# Definición de la clase Consulta que almacena información de una consulta veterinaria
class Consulta:
    def __init__(self, fecha, motivo, diagnostico, mascota):
        self.fecha = fecha
        self.motivo = motivo
        self.diagnostico = diagnostico
        self.mascota = mascota

    # Método para mostrar la información de la consulta veterinaria
    def __str__(self):
        return (f"Fecha: {self.fecha}, Motivo consulta: {self.motivo}, "
                f"Diagnóstico: {self.diagnostico}")


# Lista vacía para almacenar todas las mascotas registradas
mascotas = []

# Función para registrar una nueva mascota y su dueño
def registrar_mascota():
    
    # Validación de posibles errores en la entradas de datos
    try:
        print("\n--- Registrar Nueva Mascota ---")
        nombre = input("Nombre de la mascota: ")
        especie = input("Especie: ")
        raza = input("Raza: ")
        edad = int(input("Edad: "))
        if edad < 0:
            raise ValueError("La edad no puede ser un númerio negativo.")
        
        print("\n--- Datos del Dueño ---")
        nombre_dueno = input("Nombre del dueño: ")
        telefono = input("Teléfono: ")
        direccion = input("Dirección: ")
        
        dueno = Dueno(nombre_dueno, telefono, direccion)
        mascota = Mascota(nombre, especie, raza, edad, dueno)
        mascotas.append(mascota)
        print("\n¡Mascota registrada exitosamente!\n")
        
        logging.info(f"Mascota registrada exitosamente: {mascota.nombre}, Dueño: {dueno.nombre}")
    except ValueError as ve: # Captura de errores de valor
        print(f"Error: {ve}") 
        logging.error(f"Error al registrar mascota: {ve}") # Registro del error
    except Exception as e: # Captura de errores imprevistos en tiempo de jecución
        print("Error al registrar la mascota.")
        logging.exception("Excepción general al registrar mascota.") # Registro de la excepción general       


# Función para registrar una consulta veterinaria para una mascota
def registrar_consulta():
    
    # Validación de posibles errores en la entradas de datos
    try:
        print("\n--- Registrar Consulta ---")
        if not mascotas:
            print("\nNo hay mascotas registradas.\n")
            return
        
        listar_mascotas()
        idmascota = int(input("Seleccione el número de la mascota: ")) - 1
        if not (0 <= idmascota < len(mascotas)):
            raise IndexError("Número de mascota no válido.")
        while True:
            fecha = input("Fecha (YYYY-MM-DD): ")
            try:
                datetime.strptime(fecha, "%Y-%m-%d")  # Validar formato de fecha
                break
            except ValueError:
                print("Formato de fecha inválido. Intente nuevamente.")
                
        motivo = input("Motivo de la consulta: ")
        diagnostico = input("Diagnóstico: ")
        
        consulta = Consulta(fecha, motivo, diagnostico, mascotas[idmascota])
        mascotas[idmascota].agregar_consulta(consulta)
        print("\n¡Consulta registrada exitosamente!\n")
        
        logging.info(f"Consulta registrada para {mascotas[idmascota].nombre} en {fecha}")
    except ValueError: # Captura de errores de valor
        print("Entrada inválida. Por favor ingrese un número válido.")
        logging.error("Valor inválido al seleccionar mascota para realizar consulta.") # Registro del error
    except IndexError as ie: # Captura de errores de índice
        print(f"Error: {ie}")
        logging.warning(f"El número seleccionado está fuera del rango: {ie}") # Registro del error
    except Exception as e: # Captura de errores imprevistos en tiempo de ejecución
        print("Ocurrió un error al registrar la consulta.")
        logging.exception("Excepción general al registrar consulta.") # Registro de la excepción general
        
        
# Función para mostrar todas las mascotas registradas
def listar_mascotas():
    print("\n--- Lista de Mascotas ---")
    if not mascotas:
        print("No hay mascotas registradas.\n")
        logging.info("Listado solicitado con éxito. No hay mascotas registradas") # Registro del evento ocurrido
        return
    for i, mascota in enumerate(mascotas, 1):
        print(f"{i}. {mascota}")
        

# Función para mostrar el historial de consultas veterinarias de una mascota
def ver_historial_consultas():
    
    # Validación de posibles errores en la consulta del historial
    try:
        print("\n--- Historial de Consultas ---")
        if not mascotas:
            print("\nNo hay mascotas registradas.\n")
            logging.info("Listado solicitado con éxito. No hay consultas registradas.")
            return
        
        listar_mascotas()
        idmascota = int(input("Seleccione el número (ID) de la mascota: ")) - 1
        if not (0 <= idmascota < len(mascotas)):
            raise IndexError("ID de mascota no válido.")   
             
        mascota = mascotas[idmascota]
        if not mascota.consultas:
            print("\nNo hay consultas registradas para esta mascota.\n")
            logging.info(f"No hay consultas para la mascota {mascota.nombre}")
        else:
            print(f"\nHistorial de consultas para {mascota.nombre}:")
            for consulta in mascota.consultas:
                print(consulta)
    except ValueError: # Captura de errores de valor
        print("Entrada inválida. Por favor ingrese un número válido.")
        logging.error("Valor inválido para ver historial de consultas.") # Registro del error
    except IndexError as ie: # Captura de errores de índice
        print(f"Error: {ie}")
        logging.warning(f"El índice seleccionado está fuera del rango: {ie}") # Registro del error
    except Exception as e: # Captura de errores imprevistos en tiempo de ejecución
        print("Ocurrió un error al ver el historial.")
        logging.exception("Excepción general al ver historial.") # Registro de la excepción general
        

# Función para guardar las mascotas y dueños en un archivo CSV
def guardar_mascotas_csv():
    try:
        if not mascotas:
            logging.warning("No hay mascotas registradas para guardar en el archivo CSV.")
            return
        with open(archivo_csv, mode='w', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(['nombre_mascota', 'especie', 'raza', 'edad',
                             'nombre_dueno', 'telefono', 'direccion'])
            for mascota in mascotas:
                writer.writerow([mascota.nombre, mascota.especie, mascota.raza, mascota.edad,
                                 mascota.dueno.nombre, mascota.dueno.telefono, mascota.dueno.direccion])
        logging.info("Datos de mascotas y dueños guardados en CSV exitosamente")
    except Exception as e:
        logging.exception("Error al guardar datos de mascotas y dueños en CSV.")


# Función para guardar las consultas en un archivo JSON
def guardar_consultas_json():
    try:
        if not any(m.consultas for m in mascotas):
            logging.warning("No hay consultas registradas para guardar en el archivo JSON.")
            return
        datos_consultas = []
        for mascota in mascotas:
            for consulta in mascota.consultas:
                datos_consultas.append({
                    'nombre_mascota': mascota.nombre,
                    'fecha': consulta.fecha,
                    'motivo': consulta.motivo,
                    'diagnostico': consulta.diagnostico
                })
        with open(archivo_json, mode='w', encoding='utf-8') as archivo:
            json.dump(datos_consultas, archivo, indent=4)
        logging.info("Consultas guardadas en JSON exitosamente")
    except Exception as e:
        logging.exception("Error al guardar las consultas en JSON.")
        
        
# Función para cargar mascotas y dueños desde un archivo CSV
def cargar_mascotas_csv():
    try:
        if not os.path.exists(archivo_csv):
            logging.warning("Archivo CSV de mascotas no encontrado.")
            return
        with open(archivo_csv, mode='r', encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo)
            for row in reader:
                if not all(row.values()):
                    logging.warning("Fila incompleta en el archivo CSV: {row} . Se omitirá.")
                    continue
                if any(m.nombre == row['nombre_mascota'] for m in mascotas):
                    logging.warning(f"Ya existe una mascota con el nombre {row['nombre_mascota']}. Se omitirá.")
                    continue
                dueno = Dueno(row['nombre_dueno'], row['telefono'], row['direccion'])
                mascota = Mascota(row['nombre_mascota'], row['especie'], row['raza'], int(row['edad']), dueno)
                mascotas.append(mascota)
        logging.info("Datos de mascotas y dueños cargados desde CSV exitosamente")
    except Exception as e:
        logging.exception("Error al cargar datos desde CSV.")


# Función para cargar consultas desde un archivo JSON
def cargar_consultas_json():
    try:
        if not os.path.exists(archivo_json):
            logging.warning("Archivo JSON de consultas no encontrado.")
            return
        with open(archivo_json, mode='r', encoding='utf-8') as archivo:
            datos_consultas = json.load(archivo)
            for item in datos_consultas:
                mascota = next((m for m in mascotas if m.nombre == item['nombre_mascota']), None)
                if mascota:
                    consulta = Consulta(item['fecha'], item['motivo'], item['diagnostico'], mascota)
                    mascota.agregar_consulta(consulta)
        logging.info("Consultas cargadas desde JSON exitosamente")
    except Exception as e:
        logging.exception("Error al cargar consultas desde JSON.")


# Menú principal de la aplicación
def menu():
    logging.info("Inicio de la aplicación.") # Registro del inicio de la aplicación
    while True:
        print("\n--- Clínica Veterinaria Amigos Peludos ---")
        print("1. Registrar mascota")
        print("2. Agendar consulta")
        print("3. Listar mascotas")
        print("4. Ver historial de consultas de una mascota específica")
        print("5. Exportar datos (CSV/JSON)")
        print("6. Importar datos (CSV/JSON)")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")
        
        # Validación de posibles errores en la entrada del menú
        try:
            if opcion == "1":
                registrar_mascota()
            elif opcion == "2":
                registrar_consulta()
            elif opcion == "3":
                listar_mascotas()
            elif opcion == "4":
                ver_historial_consultas()
            elif opcion == "5":
                guardar_mascotas_csv()
                guardar_consultas_json()
                print("Datos exportados exitosamente.")
            elif opcion == "6":
                if mascotas:  # Verifica si hay mascotas registradas antes de importar
                    confirmacion = input("¿Está seguro de que desea importar datos? Esto sobrescribirá los datos actuales (S/N): ").lower()
                    if confirmacion != 's':
                        print("Importación cancelada.")
                        logging.info("Importación de datos cancelada por el usuario.")
                        continue
                    mascotas.clear()  # Esto evita duplicados al cargar los archivos
                cargar_mascotas_csv()
                cargar_consultas_json()
                print("\n¡Datos importados exitosamente!")
            elif opcion == "7":
                print("¡Hasta luego!")
                logging.info("Cierre de la aplicación.")  # Registro del cierre de la aplicación
                break
            else:
                print("Opción inválida. Intente de nuevo.\n")
        except Exception as e: # Captura de errores imprevistos en tiempo de ejecución
            print("Error en el menú principal.")
            logging.exception("Error en el menú principal") # Registro de la excepción general


# Punto de entrada de la aplicación
if __name__ == "__main__":
    
    # Cargar datos de mascotas y consultas al iniciar la aplicación
    # cargar_mascotas_csv()
    # cargar_consultas_json()
    
    # Iniciar el menú principal de la aplicación
    menu()
    
    # Guardar los datos de mascotas y consultas al cerrar la aplicación
    guardar_mascotas_csv()
    guardar_consultas_json()