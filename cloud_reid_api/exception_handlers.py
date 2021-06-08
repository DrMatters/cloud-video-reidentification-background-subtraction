from starlette.responses import JSONResponse


async def expired_signature_exception_handler(request, exc):
    return JSONResponse({
        'status': 'error',
        'payload': str(exc),
    }, status_code=401)


async def wrong_credentials(request, exc):
    return JSONResponse({
        'status': 'error',
        'payload': str(exc),
    }, status_code=401)


async def entity_not_found(request, exc):
    return JSONResponse({
        'status': 'error',
        'payload': str(exc),
    }, status_code=404)
