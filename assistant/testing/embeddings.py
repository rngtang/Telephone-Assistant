from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import OpenAI
from langchain.chains import VectorDBQA
from langchain_community.document_loaders import TextLoader

loader = TextLoader('state_of_the_union.txt')
documents = loader.load()