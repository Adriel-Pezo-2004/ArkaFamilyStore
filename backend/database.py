from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import logging
from werkzeug.security import generate_password_hash, check_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    _instance = None
    
    def __init__(self):
        if not DatabaseManager._instance:
            try:
                self.client = MongoClient('mongodb://localhost:27017')
                self.db = self.client['Arka']
                self.collection = self.db['Catalogo']
                self.users_collection = self.db['Usuarios']
                
                # Crear índice de texto
                self.collection.create_index([("nombre", "text"), ("descripcion", "text"), ("categoria", "text")])
                
                DatabaseManager._instance = self
                logger.info("Successfully connected to MongoDB and created text index")
            except Exception as e:
                logger.error(f"Error connecting to MongoDB: {str(e)}")
                raise

    def search_catalog(self, search_term):
        try:
            # Primero, registramos el término de búsqueda
            logger.info(f"Buscando término: '{search_term}'")
            
            # Realizar la búsqueda
            query = {"$text": {"$search": search_term}}
            
            # Registrar la consulta
            logger.info(f"Query ejecutada: {query}")
            
            # Realizar la búsqueda y convertir a lista
            results = list(self.collection.find(query))
            
            # Registrar cantidad de resultados
            logger.info(f"Cantidad de resultados encontrados: {len(results)}")
            
            # Si no hay resultados, intentar una búsqueda más flexible
            if not results:
                logger.info("No se encontraron resultados con búsqueda de texto, intentando búsqueda regex")
                regex_query = {
                    "$or": [
                        {"nombre": {"$regex": search_term, "$options": "i"}},
                        {"descripcion": {"$regex": search_term, "$options": "i"}},
                        {"categoria": {"$regex": search_term, "$options": "i"}}
                    ]
                }
                results = list(self.collection.find(regex_query))
                logger.info(f"Resultados con regex: {len(results)}")
            
            formatted_results = []
            for result in results:
                formatted_result = {
                    "_id": str(result["_id"]),
                    "nombre": result.get("nombre", ""),
                    "descripcion": result.get("descripcion", ""),
                    "precio": result.get("precio", 0),
                    "categoria": result.get("categoria", ""),
                    "imagen": result.get("imagen", "")
                }
                formatted_results.append(formatted_result)
                logger.info(f"Documento formateado: {formatted_result}")
            
            return formatted_results
        except Exception as e:
            logger.error(f"Error searching catalog: {str(e)}")
            raise

    def count_documents(self):
        try:
            count = self.collection.count_documents({})
            logger.info(f"Total documents in collection: {count}")
            return count
        except Exception as e:
            logger.error(f"Error counting documents: {str(e)}")
            raise