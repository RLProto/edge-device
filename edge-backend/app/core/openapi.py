from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def add_custom_openapi_schema(app: FastAPI) -> None:
    """
    Adiciona um schema de configurações personalizadas para o OpenAPI

    Args:
        app: instancia do FastAPI

    Returns:
        None: Não retorna nada

    Examples:
        >>> add_custom_openapi_schema(FastAPI())
    """
    if app.openapi_schema:
        return
    openapi_schema = get_openapi(
        title="Soda Vision AutoML API",
        version="1.0.0",
        description="API do Soda Vision AutoML",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
