import requests

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVlMWM2NGNmYTdkZDYyNzVhYjBmMjgxMyIsImlhdCI6MTYyNjg2ODE4OH0.qCmS7c3JbVkejpGXn1lCnDaz7WPApRtF9sEsCtlYLnU'

endpoint = 'https://api.leasing-trade.ru:4000/graphql'
headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}

query = """
query{
  allCompanies (filter:{}){
    id
    name
    inn
  }
}
"""

r= requests.post(endpoint, json={"query": query}, headers=headers)
if r.status_code == 200:
    print(r.json())
else:
    print("error! status: ", r.status_code)