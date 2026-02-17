try:
    from django.http import HttpResponsePermanentRedirect  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    def HttpResponsePermanentRedirect(*_args, **_kwargs):
        raise RuntimeError("Django is required to use WwwToRootRedirectMiddleware.")


class WwwToRootRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(":")[0].lower()
        if host == "www.jmviews.co.uk":
            return HttpResponsePermanentRedirect(
                "https://jmviews.co.uk" + request.get_full_path()
            )
        return self.get_response(request)