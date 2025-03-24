from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Optional, Any, Dict


class BaseMongoService:
    def __init__(self, db_client: MongoClient, collection_name: str, db_name: str = "DataProfiling"):
        """
        Initialize the BaseMongoService with a MongoDB client, database name, and collection name.
        """
        self.collection: Collection = db_client[db_name][collection_name]

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new document in the collection.
        """
        result = self.collection.insert_one(data)
        return {"inserted_id": str(result.inserted_id)}
    
    def create_many(self, data: list[Dict]) -> list[Dict]:
        """
        Create a new document in the collection.
        """
        result = self.collection.insert_many(data)
        return {"inserted_ids": str(result.inserted_ids)}

    def get_by_id(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a document by its ID.
        """
        if not ObjectId.is_valid(document_id):
            raise ValueError("Invalid ObjectId")
        
        document = self.collection.find_one({"_id": ObjectId(document_id)})
        if document:
            document["_id"] = str(document["_id"])  # Convert ObjectId to string
        return document

    def update(self, document_id: str, updated_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing document by its ID.
        """
        if not ObjectId.is_valid(document_id):
            raise ValueError("Invalid ObjectId")
        
        result = self.collection.update_one(
            {"_id": ObjectId(document_id)},
            {"$set": updated_data}
        )
        if result.matched_count == 0:
            return {"error": "Document not found"}
        
        return {"message": "Document updated successfully"}

    def delete(self, document_id: str) -> Dict[str, Any]:
        """
        Delete a document by its ID.
        """
        if not ObjectId.is_valid(document_id):
            raise ValueError("Invalid ObjectId")
        
        result = self.collection.delete_one({"_id": ObjectId(document_id)})
        if result.deleted_count == 0:
            return {"error": "Document not found"}
        
        return {"message": "Document deleted successfully"}

    def get_all(self, query: Optional[Dict[str, Any]] = None, fields: Optional[Dict[str, int]] = None) -> list:
        """
        Retrieve all documents matching a query with optional field selection.
        :param query: The query to filter documents.
        :param fields: A dictionary specifying the fields to include or exclude (e.g., {"field_name": 1} to include or {"field_name": 0} to exclude).
        """
        query = query or {}
        fields = fields or {}  # Default to no field selection (return all fields)
        documents = list(self.collection.find(query, fields))
        for document in documents:
            document["_id"] = str(document["_id"])  # Convert ObjectId to string
        return documents
    
    def get_all_with_pagination(self, query: Optional[Dict[str, Any]] = None, page_size: int = 10, page_number: int = 1) -> list:
        """
        Retrieve all documents matching a query with pagination.
        """
        query = query or {}
        skip = (page_number - 1) * page_size
        documents = list(self.collection.find(query).skip(skip).limit(page_size))
        for document in documents:
            document["_id"] = str(document["_id"])  # Convert ObjectId to string
        return documents