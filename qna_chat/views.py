from django.http import JsonResponse
from django.shortcuts import render
from .langchain import DjangLangRAG
from .scrape_urls import get_drf_urls


def index(request):
    """
    Returns JSON as response to a user query.
    """
    if request.method == "POST":
        query = request.data.get("query")
        # TODO: initialize results
        result = {}
        return JsonResponse(result)
    return render(request, "index.html")


def create_db(request):
    drf_urls = get_drf_urls()

    djanglang = DjangLangRAG()
    if djanglang.check_db():
        status = {
            "exists": "database exists",
            "message": ("Database exists"),
        }
        return JsonResponse(status)

    djanglang.init_db.delay(drf_urls, "drf")
    return JsonResponse({"status": "Building database..."})
