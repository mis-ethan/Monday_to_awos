import httpx
import os
import json
from fastapi import FastAPI
from fastapi import HTTPException

API_KEY = os.getenv("MONDAY_API_TOKEN")
IPAD_BOARD = os.getenv("IPAD_DEPLOYMENT_BOARD")
REQUEST_GROUP = "group_mkt4473j"

MONDAY_API_URL = 'https://api.monday.com/v2'


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to my API: " + API_KEY}


@app.get("/create-workorders/")
async def get_group_items():
    board_id = IPAD_BOARD
    group_id = REQUEST_GROUP
    query = """
    query ($board_id: ID!, $group_id: String!) {
      boards(ids: [$board_id]) {
        groups(ids: [$group_id]) {
          items_page{
            items {
              id
              name
              column_values {
                id
                text
              }
            }
          }
        }
      }
    }
    """
    variables = {"board_id": board_id, "group_id": group_id}

    HEADERS = {'Authorization': API_KEY,
              "Content-Type": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            MONDAY_API_URL,
            json={"query": query, "variables": variables},
            headers = HEADERS,
        )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error from Monday API")

    data = response.json()
    try:
        items = data["data"]["boards"][0]["groups"][0]["items_page"]["items"]
        return items
        result = []
        for item in items:
            result.append({
                "item_id": item["id"],
                "name": item["name"],
                "columns": {col["title"]: col["text"] for col in item["column_values"]}
            })
        return result
    except (KeyError, IndexError) as e:
        raise HTTPException(status_code=500, detail="Error parsing Monday API response")
