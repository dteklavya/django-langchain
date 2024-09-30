## Django-LangChain

This is fun Django project integrating LangChain for building a simple RAG (Retrieval-Augmented Generation) chatbot. Goal is to create a chatbot capable of answering questions based on [Django REST Framework documentation](https://www.django-rest-framework.org/).

# Overview

* Scrape all links from [DRF Documentation](https://www.django-rest-framework.org/) page.
* Create Chroma database processing all docs as back-end job using Celery
* Retrieve content from DB matching user query.
