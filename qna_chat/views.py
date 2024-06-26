from django.http import JsonResponse
from django.shortcuts import render
from .langchain import DjangLangRAG
from .scrape_urls import get_drf_urls
from celery.result import AsyncResult


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
    djanglang = DjangLangRAG()
    if djanglang.check_db():
        status = {
            "exists": "database exists",
            "message": ("Database exists"),
        }
        return JsonResponse(status)

    drf_urls = get_drf_urls()

    djanglang.init_db.delay(drf_urls, "drf")
    return JsonResponse({"status": "Building database..."})


def check_task_status(request):
    task_id = request.GET.get("task_id")
    result = AsyncResult(task_id)
    response_data = {"status": result.status, "result": result.result}
    return JsonResponse(response_data)
