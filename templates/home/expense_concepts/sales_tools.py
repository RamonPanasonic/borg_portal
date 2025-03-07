import requests
import json
from SalesAgents.sales_agents import sales_agent


def OdooSaleOrderTool(session_id, payload, ENDPOINT_ODOO):
  if not session_id:
      return json.dumps({"error": "Session ID is required."})
  
  headers = {"Content-Type": "application/json", "Cookie": f"session_id={session_id}"}

  try:
      response = requests.post(ENDPOINT_ODOO, json=payload, headers=headers)
      response.raise_for_status()
      result = response.json()

      print(result)

      if not result.get("result"):
          return json.dumps({"message": "No information found."})

      return json.dumps({"status": "success", "data": result["result"]})

  except requests.RequestException as e:
      return json.dumps({"error": f"Error contacting Odoo: {str(e)}"})
    

payload = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "model": "sale.order",
        "method": "search_read",
        "args": [
            [
                ["state", "=", "cancel"],
                ["date_order", ">=", "2024-02-01"],
                ["date_order", "<", "2024-03-01"]
            ]
        ],
        "kwargs": {
            "fields": ["id", "amount_total"],
            "limit": 1000
        }
    }
}

payload = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "model": "account.move",
        "method": "search_read",
        "args": [
            [["partner_id", "=", 68002], ["move_type", "=", "out_invoice"]]
        ],
        "kwargs": {
            "fields": ["id", "name", "invoice_date", "state", "amount_total", "currency_id"],
            "limit": 100
        }
    }
}

#print(OdooSaleOrderTool('70c4efaecdab369c74667a681bdd0de70081d949',payload, 'http://yokosuka.odoo.com/web/dataset/call_kw'))