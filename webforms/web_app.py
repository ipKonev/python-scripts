import uvicorn
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from socket import gethostbyname
from typing import Optional
from pydantic import BaseModel

from mass_dacl_update import *

#class Domain_names(BaseModel):
#    names: str

app=FastAPI()

@app.get("/")
async def start():
    return FileResponse('page.html') 

@app.post("/postdata/")
async def lookup_dns(pattern: str = Form(...), addresses: str = Form(...), ticket: str = Form(...)):
    verified_addresses = [addr.strip() for addr in addresses.split(',')]
    if verified_addresses[0] == '': 
        return FileResponse('error-page.html')
    elif ('VPN-Konev' not in pattern): 
        return FileResponse('error-page.html')

    values=getalldacl()
    for dacl_name,dacl_id in values.items():
        if pattern in dacl_name:
            current_content=get_content(get_by_id(dacl_id))
            content = add_content(current_content,verified_addresses,ticket=ticket,dacl_name=dacl_name)
            uniq_content = uniq_content_verif(content)
            put_content(dacl_name,dacl_id,uniq_content)
    return pattern, verified_addresses, ticket
    #lookup = lambda x: gethostbyname(x)
    #return list(map(lookup,domain_names.names.split(',')))



if __name__ == '__main__':
    uvicorn.run('web_app:app', host='10.120.15.13', port=8000)
