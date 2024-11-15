import json
import sys

from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
from urllib.parse import urlparse

SCOPES = "https://www.googleapis.com/auth/documents.readonly"
DISCOVERY_DOC = "https://docs.googleapis.com/$discovery/rest?version=v1"

docurl = ""

def help():
    print(f"Usage: {sys.argv[0]} [document url]")
    
def decode(docId):
    print(f"getting contents of Google Doc ID {docId}")
    
    # initialise credentials and instantiate Google Docs API service
    try:
        store = file.Storage("token.json")
        creds = store.get()
        
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
            creds = tools.run_flow(flow, store)
    except Exception:
        print("credentials not found")
        
    service = discovery.build(
        "docs",
        "v1",
    #    http=creds.authorize(Http()),
       discoveryServiceUrl=DISCOVERY_DOC
    )
    
    # request document and print results as formatted JSON
    result = service.documents().get(documentId=docId, includeTableContent=True).execute()
    print(json.dumps(result, indent=4, sort_keys=True))

if len(sys.argv) < 2:
    help()
    sys.exit()
    
docurl = sys.argv[1]
parsed = urlparse(sys.argv[1])
decode(parsed.path)
