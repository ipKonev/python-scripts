import uvicorn
from fastapi import FastAPI
from socket import gethostbyname
from typing import Optional
from pydantic import BaseModel

class Domain_names(BaseModel):
    names: str

app=FastAPI()

@app.post("/lookup_names/")
async def lookup_dns(domain_names: Domain_names):
    lookup = lambda x: gethostbyname(x)
    return list(map(lookup,domain_names.names.split(',')))



if __name__ == '__main__':
    uvicorn.run('lookup_names:app', host='10.255.255.255', port=8000)
