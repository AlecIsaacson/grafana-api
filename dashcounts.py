import requests
import json

baseURL = "https://YourOrgSlug.grafana.net"
apiKey = "yourAPIKeyHere"

# Initialize search args and page
searchApi = '/api/search'
searchArgs = '?limit=1000&page='
searchPage = 1

totalDashCount = 0
totalFolderCount = 0
dictDashboards = []

# This function hits the API, gets the JSON structure with the dashboard names and such, and returns a dict with that info.
def queryDashboardInfo(searchPage):
    dictDashboards = []
    searchUrl = baseURL + searchApi + str(searchArgs) + str(searchPage)
    headers = {"Authorization": "Bearer " + apiKey}
    # print(headers)
    response = requests.get(searchUrl, headers=headers)
    dictDashboards = json.loads(response.text)
    # Uncomment the line below to see the whole JSON structure.
    # print(json.dumps(dictDashboards, indent=2))
    return(dictDashboards)

# Here we take the dict of dashboard info an generate the counts of dashboards and folders.
# Note that some "dashboard folders" are actually used by K6 and not seen in the dashboards UI.  The logic below excludes them from the count.
def processDashboardInfo(dictDashboards):
    pageDashCount = 0
    pageFolderCount = 0
    for dashboardTitles in dictDashboards:
        if dashboardTitles['type'] == "dash-db":
            pageDashCount += 1
        if (dashboardTitles['type'] == "dash-folder") and (dashboardTitles.get('folderUid') != "k6-app" and dashboardTitles.get('uid') != "k6-app"):
            pageFolderCount += 1
    # print(pageDashCount, pageFolderCount)
    return pageDashCount, pageFolderCount

# Main routine
# Get the first round of dashboards and generate the counts.
dictDashboards = queryDashboardInfo(searchPage)
pageDashCount, pageFolderCount = processDashboardInfo(dictDashboards)

# Start to accumulate the totals.
totalFolderCount += pageFolderCount
totalDashCount += pageDashCount

# See if there's another page, if there is, keep going until we get a page with zero results.
while pageDashCount != 0:
    # Conn, Sonar - we are paginating
    print("Querying page: " + str(searchPage))
    # We already got page 1 in the lines above.
    searchPage += 1

    dictDashboards = queryDashboardInfo(searchPage)
    pageDashCount, pageFolderCount = processDashboardInfo(dictDashboards)

    totalFolderCount += pageFolderCount
    totalDashCount += pageDashCount

# Done! Print the output.
print("")
print("Dasboard count = " + str(totalDashCount) + " Folder count = " + str(totalFolderCount))