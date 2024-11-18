"""Utilizing mongodb features for the project."""
from motor.motor_asyncio import AsyncIOMotorClient


class MongoDBAsync:
    def __init__(self, uri: str, db_name: str, collection_name: str):
        """
        Initialize the MongoDBAsync object with connection details.
        """
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

    async def connect(self):
        """
        Establish a connection to the MongoDB database and collection.
        """
        self.client = AsyncIOMotorClient(self.uri)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    async def insert_one(self, document: dict):
        """
        Insert a single document into the collection.
        """
        await self.collection.insert_one(document)

    async def insert_many(self, documents: list):
        """
        Insert multiple documents into the collection.
        """
        filtered_document_list = []

        try:
            for i in documents:
                existing_document = await self.find_one({'stock_code': i.get('stock_code')})
                if not existing_document:
                    filtered_document_list.append(i)
            
            if filtered_document_list:
                await self.collection.insert_many(filtered_document_list)
        except Exception as e:
            print(f"Error: {e}")
        # await self.collection.insert_many()

    async def find_one(self, query: dict):
        """
        Find a single document that matches the query.
        """
        result = await self.collection.find_one(query)

        return result

    async def find_all(self, query: dict = {}):
        """
        Find all documents that match the query.
        """
        cursor = self.collection.find(query)
        documents = []
        async for document in cursor:
            documents.append(document)

        return documents

    async def close(self):
        """
        Close the connection to MongoDB.
        """
        if self.client:
            self.client.close()
