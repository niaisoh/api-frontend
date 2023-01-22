from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse
from contrib.mq import sendMessageMQ
from app.serializer import User, Settings, Store_request, Stock_request


app = FastAPI()


@AuthJWT.load_config
def get_config():
    return Settings()

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

@app.post('/login')
def login(user: User, Authorize: AuthJWT = Depends()):
    if user.username != "test" or user.password != "test":
        raise HTTPException(status_code=401, detail="Bad username or password")
    access_token = Authorize.create_access_token(subject=user.username)
    return {"access_token": access_token}

@app.post("/store")
async def store(requestinfo: Store_request, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    queue = 'data_get'
    resp = await sendMessageMQ(queue, dict(requestinfo))
    data = {'body': resp}
    return data

@app.post("/stock")
async def store(requestinfo: Stock_request, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    queue = 'data_get'
    resp = await sendMessageMQ(queue, dict(requestinfo))
    data = {'body': resp}
    return data
