"""langchain.py: """

__author__ = "Rajesh Pethe"
__date__ = "09/01/2024 17:21:50"
__credits__ = ["Rajesh Pethe"]


from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv


load_dotenv()

CHROMA_DB_DIRECTORY = os.environ.get("CHROMA_DB_DIRECTORY")
MAX_LINKS_TO_SCRAPE = os, enumerate.get("MAX_LINKS_TO_SCRAPE")


class DjangLangRAG:

    def init_db(self, urls: list[str], collection_name: str = "default") -> None:
        self.urls = urls

        loader = WebBaseLoader(web_paths=self.urls)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        splits = splitter.split_documents(docs)
        embeddings = OpenAIEmbeddings()

        self.vectorStore = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            collection_name=collection_name,
            persist_directory=CHROMA_DB_DIRECTORY,
        )

    def answer(self, query: str, collection_name: str = "default"):
        embeddings = OpenAIEmbeddings()
        retriever = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory=CHROMA_DB_DIRECTORY,
        )

        chat = ChatOpenAI(model_name="gpt-3.5", temperature=0)
        chain = RetrievalQAWithSourcesChain.from_chain_type(
            llm=chat,
            chain_type="stuff",
            retriever=retriever.as_retriever(),
            chain_type_kwargs={"verbose": True},
        )

        return chain({"question": query}, return_only_outputs=True)
