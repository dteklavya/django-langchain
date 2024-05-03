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
from time import sleep
from bs4 import BeautifulSoup
from typing import Union
from celery import shared_task


load_dotenv()

CHROMA_DB_DIRECTORY = os.environ.get("CHROMA_DB_DIRECTORY")
MAX_LINKS_TO_SCRAPE = os.environ.get("MAX_LINKS_TO_SCRAPE")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class CustomLoader(WebBaseLoader):
    def _scrape(
        self,
        url: str,
        parser: Union[str, None] = None,
        bs_kwargs: dict = {},
    ):
        html_content = super()._scrape(url, parser)
        main_content = html_content.find("div", id="main-content")
        return BeautifulSoup(main_content.text, "html.parser", **bs_kwargs)


class DjangLangRAG:

    @shared_task
    def init_db(self, urls: list[str], collection_name: str = "default") -> None:

        # Check if DB already exists
        if self.check_db():
            print("Database exists. Exiting...")
            return

        self.urls = urls

        loader = CustomLoader(web_paths=self.urls)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=1000, chunk_overlap=100
        )
        splits = splitter.split_documents(docs)
        total_docs = len(splits)
        batch_size = 4
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

        for batch_start in range(0, total_docs, batch_size):
            batch_end = min(batch_start + batch_size, total_docs)
            batch_docs = splits[batch_start:batch_end]

            print("Begin loading...")
            Chroma.from_documents(
                documents=batch_docs,
                embedding=embeddings,
                collection_name=collection_name,
                persist_directory=CHROMA_DB_DIRECTORY,
            )
            print(f"Inserted {batch_end}/{total_docs} chunks. Sleeping for 60...")
            sleep(60)

        print(f"Completed inserting docs for {collection_name}")

    def answer(self, query: str, collection_name: str = "default"):
        embeddings = OpenAIEmbeddings()
        retriever = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory=CHROMA_DB_DIRECTORY,
        )

        chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        chain = RetrievalQAWithSourcesChain.from_chain_type(
            llm=chat,
            chain_type="stuff",
            retriever=retriever.as_retriever(),
            chain_type_kwargs={"verbose": True},
        )

        return chain({"question": query}, return_only_outputs=True)

    def check_db(self):
        return os.path.exists(CHROMA_DB_DIRECTORY)
