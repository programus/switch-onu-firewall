from nicegui import (
    app,
    ui,
)
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


unrestricted_page_routes = {
    '/login',
    '/static',
    '/favicon.ico',
}

class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        request_path = request.url.path
        if not app.storage.user.get('authenticated') and not request_path.startswith('/_nicegui') and request_path not in unrestricted_page_routes:
            return RedirectResponse(url=f'/login?redirect_to={request_path}')
        return await call_next(request)
