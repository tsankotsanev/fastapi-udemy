from fastapi import APIRouter, Depends, Request
from custom_log import log


router = APIRouter(
    prefix="/dependencies", tags=["dependencies"], dependencies=[Depends(log)]
)


def convert_params(request: Request, sep: str = "--"):
    query = []
    for key, value in request.query_params.items():
        query.append(f"{key} {sep} {value}")
    return query


def convert_headers(
    request: Request, sep: str = "--", query=Depends(convert_params)
):
    out_headers = []
    for header, value in request.headers.items():
        out_headers.append(f"{header} {sep} {value}")
    return {"headers": out_headers, "query": query}


@router.get("")
def get_items(headers: list = Depends(convert_headers)):
    return {"items": ["a", "b", "c"], "headers": headers}


@router.post("/new")
def create_item(sep: str = "--", headers: list = Depends(convert_headers)):
    return {"result": "new item created", "headers": headers}


class Account:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


@router.post("/user")
def create_user(account: Account = Depends()):
    return {"result": "new user created", "account": account}
