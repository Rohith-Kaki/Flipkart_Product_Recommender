#converting documents into to emdeddings
from langchain_astradb import AstraDBVectorStore 
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from flipkart.data_converter import DataConverter
from flipkart.config import Config

class DataIngestion:
    def __init__(self):
        self.embedding_model = HuggingFaceEndpointEmbeddings(model=Config.EMBEDDING_MODEL)
        self.vector_store = AstraDBVectorStore(
            embedding = self.embedding_model,
            collection_name = "flipkart_product_recommendation",
            api_endpoint = Config.ASTRA_DB_API_ENDPOINT,
            token = Config.ASTRA_DB_APPLICATION_TOKEN,
            namespace = Config.ASTRA_DB_KEY_SPACE
        )
    
    def ingest(self, load_existing=True):
        if load_existing == True:
            return self.vector_store
        docs = DataConverter('data/flipkart_product_review.csv').convert()
        self.vector_store.add_documents(docs)
        return self.vector_store
