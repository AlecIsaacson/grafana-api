import requests
import json

baseURL = "https://YourOrgSlug.grafana.net/api/search?query="
apiKey = "yourAPIKeyHere"

headers = {"Authorization": "Bearer " + apiKey}
print(headers)

response = requests.get(baseURL, headers=headers)
dictDashboards = json.loads(response.text)

# Uncomment the line below to see the whole JSON structure.
# print(json.dumps(dictDashboards, indent=2))

# print(dictDashboards)

dashCount = 0
folderCount = 0
for dashboardTitles in dictDashboards:
    if dashboardTitles['type'] == "dash-db":
        dashCount += 1
    if (dashboardTitles['type'] == "dash-folder") and (dashboardTitles.get('folderUid') != "k6-app" and dashboardTitles.get('uid') != "k6-app"):
        folderCount += 1

print("Found " + str(dashCount) + " dashboards")
print("Found " + str(folderCount) + " folders")