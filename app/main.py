from fastapi import FastAPI
from app.db.db import engine
from app.db import models
from app.api.routers import router
from app.security import cors

# logging.config.fileConfig('logger.conf', disable_existing_loggers=False)
# logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

cors.add_cors(app)
app.include_router(router)


@app.get('/')
async def front():
    # logger.info("logging from the root logger")
    return "Lieber Arthur, du bist ein kleiner Pisser :)!"
