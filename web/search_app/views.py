"""Search view.

P1 provides the route and template hookup.
P2 fills in the actual PyLucene search + ranking logic
(see search_app.search_helper for the JVM/searcher boundary).
"""
from django.conf import settings
from django.shortcuts import render

from .search_helper import search as run_search


def search_page(request):
    query = (request.GET.get('q') or '').strip()
    results = []
    error = None

    if query:
        try:
            results = run_search(query, top_k=settings.SEARCH_TOP_K)
        except NotImplementedError as exc:
            error = str(exc)

    context = {
        'query': query,
        'results': results,
        'error': error,
        'top_k': settings.SEARCH_TOP_K,
    }
    return render(request, 'search_app/search.html', context)
