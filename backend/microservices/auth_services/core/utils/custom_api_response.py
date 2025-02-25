from fastapi.responses import JSONResponse


def api_response(title, **kwargs):
    return JSONResponse(
        status_code=200, content={"message": "ok", "title": title, **kwargs}
    )
