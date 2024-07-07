from fastapi.responses import JSONResponse

def success_response(data):
    return {"status": "success", "data": data}

def error_response(message: str, status_code: int = 400):
    return JSONResponse(content={"status": "error", "message": message}, status_code=status_code)
