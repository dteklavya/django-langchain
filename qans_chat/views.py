from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    """
    Returns JSON as response to a user query.
    """
    if request.method == "POST":
        query = request.data.get("query")
        # TODO: initialize results
        result = {}
        return JsonResponse(result)
    return render(request, "base/index.html")
