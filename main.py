import httpx
import os
import json
from fastapi import FastAPI
from fastapi import HTTPException

#board and group info
API_KEY = os.getenv("MONDAY_API_KEY")
BOARD_ID = os.getenv("MONDAY_BOARD_ID")
REQUEST_GROUP = "MONDAY_GROUP_ID"

MONDAY_API_URL = 'https://api.monday.com/v2'

#enter ids of all columns wanted in return
column_ids = ["text"]

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to my API: " + API_KEY}


@app.get("/create-workorders/")
async def get_group_items():
    board_id = BOARD_ID
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
                column{
                  title
                }
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
        result = []
        i=1
        col_vals = {"item_num": f"# {i} \n"}
        for item in items:
            i+=1
            for col_id in column_ids
              for col in item["column_values"]:
                if col["id"] == col_id:
                  col_vals.append({col["column"]["text"] : col["text"]})
            result.append(col_vals)
            
        return result
    except (KeyError, IndexError) as e:
        raise HTTPException(status_code=500, detail="Error parsing Monday API response")
