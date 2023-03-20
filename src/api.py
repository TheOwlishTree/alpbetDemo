from fastapi import FastAPI
from pydantic import BaseModel, AnyHttpUrl
from src.app import WebCrawler

api = FastAPI(docs_url="/")


class RequestBody(BaseModel):
    url: AnyHttpUrl
    max_depth: int
    max_ext: int
    unique: bool


@api.post("/crawler")
async def web_crawler(body: RequestBody):
    WebCrawler(body.max_ext, body.max_depth, body.unique).run(body.url)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(api)
