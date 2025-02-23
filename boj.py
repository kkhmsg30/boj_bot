import http.client
import json

def get_profile(boj_handle:str) -> dict:
    conn = http.client.HTTPSConnection("solved.ac")
    headers = { 'Content-Type': "application/json" }
    conn.request("GET", "/api/v3/user/show?handle="+boj_handle, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

def get_problems(query:str) -> dict:
    conn = http.client.HTTPSConnection("solved.ac")
    headers = { 'Content-Type': "application/json" }
    conn.request("GET", r"/api/v3/search/problem?query="+query, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

def is_solved(problem:str, boj_handle:str) -> bool:
    conn = http.client.HTTPSConnection("solved.ac")
    headers = { 'Content-Type': "application/json" }
    conn.request("GET", f"/api/v3/search/problem?query=id%3A{boj_handle}%20s%40{id}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return bool(json.loads(data.decode("utf-8"))['count'])