class InternalServerError(Exception):
    pass

errors = {
    "InternalServerError": {
        "error" : "Internal Server Error",
        "message": "Something went wrong",
        "status": 500
    }
}