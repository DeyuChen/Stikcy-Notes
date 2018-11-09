#!/usr/bin/env python

import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json
from google.cloud import datastore

HOST_NAME = "localhost"
PORT_NUMBER = 9999
MAX_NUM_OF_NOTES = 20
MAX_CHAR_PER_NOTE = 50
KIND = "Note"

def getNotes(url):
    key = client.key(KIND, url)
    notes = client.get(key)
    if not notes:
        notes = datastore.Entity(key=key)
        notes["notes"] = []
        client.put(notes)
    
    return notes["notes"]

def sendNote(url, note):
    if len(note) > MAX_CHAR_PER_NOTE:
        note = note[:MAX_CHAR_PER_NOTE]
    
    key = client.key(KIND, url)
    with client.transaction():
        notes = client.get(key)
        notes["notes"].append(note)
        while len(notes["notes"]) > MAX_NUM_OF_NOTES:
            del notes["notes"][0]
        client.put(notes)

    return notes["notes"]

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        content = "<p>Hello</p>"
        s.wfile.write(content.encode("utf-8"))
    def do_POST(s):
        s.send_response(200)
        s.end_headers()
        text = s.rfile.read(int(s.headers["Content-Length"])).decode("utf-8")
        fields = json.loads(text)
        if "url" in fields:
            url = fields["url"]
            result = urlparse(url)
            path = result.netloc + result.path
            if "note" in fields and fields["note"]:
                note = fields["note"]
                notes = sendNote(path, note)
            else:
                notes = getNotes(path)
            
            if len(notes) > 0:
                response = "\n▶ ".join(notes)
                response = "▶ " + response
            else:
                response = "Leave a note ☺"
            s.wfile.write(response.encode("utf-8"))
                

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("need datastore service account json path")
        exit()
    
    client = datastore.Client.from_service_account_json(sys.argv[1])
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
