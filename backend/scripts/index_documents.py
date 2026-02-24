import os
import glob
import logging
from dotenv import load_dotenv
from sqlalchemy import exc
load_dotenv(override=True)

# document loader and splitter
from langchain_community.document_loaders import PyPDFLoader, pdf
from langchain_text_splitters import RecursiveCharacterTextSplitter

# azure component import
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_community.vectorstores import AzureSearch

# setup logging
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s - %(levelname)s -%(message)s"
)

logger = logging.getLogger("indexer")

def index_docs():
    '''
    Read the PDFs, chunks them, and upload them to Azure AI Search
    '''

    # define paths, we look for data folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(current_dir, "..", "data")

    # validate the required environment variables
    required_vars = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY",
        "AZURE_AI_SEARCH_ENDPOINT",
        "AZURE_AI_SEARCH_API_KEY",
        "AZURE_AI_SEARCH_INDEX_NAME"
    ]

    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Missing required environment variables : {missing_vars}")
        logger.error("Please check your .env file and ensure all variables are set")
        return

    #  initialize the embedding model : turn text into chunks
    try:
        logger.info("Initializing Azure Open AI Embedding Model")
        embeddings = AzureOpenAIEmbeddings(
            azure_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key = os.getenv("AZURE_OPENAI_API_KEY"),
            openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        )
        logger.info("Embedding model initialize successfully")
    except Exception as e:
        logger.error(f"Failed to initialize the embeddings : {e}")
        logger.error("Please verify the Azure Open AI deployment name and endpoints")

    index_name = os.getenv("AZURE_AI_SEARCH_INDEX_NAME")
    # initialize Azure Search
    try:
        logger.info("Initializing Azure AI Search vector store")
        vector_store = AzureSearch(
            azure_search_endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT"),
            azure_search_key = os.getenv("AZURE_AI_SEARCH_API_KEY"),
            index_name = os.getenv("AZURE_AI_SEARCH_INDEX_NAME"),
            embedding_function = embeddings.embed_query
        )
        logger.info(f"Vector store initialized for index : {index_name}")
    except Exception as e:
        logger.error(f"Failed to initialize the Azure Search : {e}")
        logger.error("Please verify the Azure Search Endpoints, API key and index name.")
        return

    # Find PDF files
    pdf_files = glob.glob(os.path.join(data_folder, "*.pdf"))
    if not pdf_files:
        logger.warning(f"No PDFs found in {data_folder}. Please add files")
    logger.info(f"Found {len(pdf_files)} PDFs to process : {[os.path.basename(f) for f in pdf_files]}")

    all_splits = []

    for pdf_path in pdf_files:
        try:
            logger.info(f"Loading : {os.path.basename(pdf_path)}....")
            loader = PyPDFLoader(pdf_path)
            raw_docs = loader.load()

            # chunking strategy
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size = 1000,
                chunk_overlap = 200
            )
            splits = text_splitter.split_documents(raw_docs)
            for split in splits:
                split.metadata["source"] = os.path.basename(pdf_path)

            all_splits.extend(splits)
            logger.info(f"Splits in {len(splits)} chunks.")
        
        except Exception as e:
            logger.error(f"Failed to process {pdf_path} : {e}")

        
        # Upload to Azure 
        if  all_splits:
            logger.info(f"Uploading {len(all_splits)} chunks to Azure AI Search index {index_name}")
            try:
                # azure search accepts batches automatically via this method
                vector_store.add_documents(documents=all_splits)
                logger.info("="*60)
                logger.info("Indexing Complete! Knowledge base is  ready...")
                logger.info(f"Total chunk indexed : {len(all_splits)}")
                logger.info("="*60)
            except Exception as e:
                logger.error(f"Failed to upload the documents to Azure Search : {e}")
                logger.error("Please check Azure Search configuration and try again")
        
        else:
            logger.warning("No documents were processed.")

if __name__ == "__main__":
    index_docs()