
import pandas as pd
from pymongo import MongoClient
import argparse
import os

def import_csv_to_mongo(csv_file_path, db_name, collection_name, mongo_uri="mongodb://server25.fjortega.es:27017/"):
    """
    Importa datos desde un archivo CSV a una colección de MongoDB.

    :param csv_file_path: Ruta al archivo CSV.
    :param db_name: Nombre de la base de datos de MongoDB.
    :param collection_name: Nombre de la colección de MongoDB.
    :param mongo_uri: URI de conexión de MongoDB.
    """
    if not os.path.exists(csv_file_path):
        print(f"Error: El archivo no se encontró en la ruta {csv_file_path}")
        return

    try:
        # Conectar a MongoDB
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]
        print(f"Conectado a MongoDB en {mongo_uri}")

        # Leer el archivo CSV con pandas
        df = pd.read_csv(csv_file_path)

        # Convertir el DataFrame a una lista de diccionarios (formato JSON)
        data = df.to_dict('records')

        if not data:
            print("El archivo CSV está vacío o no contiene datos.")
            return

        # Opcional: Limpiar la colección antes de insertar nuevos datos
        # collection.delete_many({})

        # Insertar los datos en la colección
        result = collection.insert_many(data)

        print(f"Importación completada con éxito.")
        print(f"Se importaron {len(result.inserted_ids)} registros.")
        print(f"Base de datos: '{db_name}'")
        print(f"Colección: '{collection_name}'")

    except pd.errors.EmptyDataError:
        print(f"Error: El archivo CSV {csv_file_path} está vacío.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        if 'client' in locals() and client:
            client.close()
            print("Conexión a MongoDB cerrada.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Importar un archivo CSV a una base de datos MongoDB local.")
    parser.add_argument("csv_file", help="Ruta al archivo CSV a importar.")
    parser.add_argument("db_name", help="Nombre de la base de datos de destino en MongoDB.")
    parser.add_argument("collection_name", help="Nombre de la colección de destino en MongoDB.")
    parser.add_argument("--uri", default="mongodb://server25.fjortega.es:27017/", help="URI de conexión de MongoDB (por defecto: mongodb://server25.fjortega.es:27017/).")

    args = parser.parse_args()

    import_csv_to_mongo(args.csv_file, args.db_name, args.collection_name, args.uri)
