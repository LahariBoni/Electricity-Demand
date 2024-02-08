import requests
import json
import pandas as pd

# API endpoint URL
# base_url = "https://api.eia.gov/v2/electricity/rto/daily-region-data/data/"
base_url="https://api.eia.gov/v2/electricity/rto/daily-fuel-type-data/data"



params = {
    "api_key": "9mtefpVPYLigJBDoeBToWDSKkfGap2RwlrTkGuTA", #please enter your api key
    "frequency": "daily", #this can be hourly,daily, monthly, yearly depends on the end point url that is base_url
    "data[0]": "value",
    "start": "2023-01-01",
    "end": "2023-12-31",
    "sort[0][column]": "period",
    "sort[0][direction]": "desc",
    "offset": 0,
    "length": 5000, #this is the max we can retrieve for each api call
}

# Initialize variables
all_data = []

# Make consecutive API calls until all records are retrieved
offset = 0
while True:
    params['offset'] = offset #updating the offset for each iteration to get the next 5k records
    response = requests.get(base_url, params=params).json()

    # Extract 'data' from the response
    data = response.get('response', {}).get('data', [])
    print(f"Rows added in this API call: {len(data)}") #this can be commented

    # Append the data to the existing list
    all_data.extend(data)

    # Increment the offset
    offset += params['length']

    # Break the loop if the retrieved data is empty
    if not data:
        break

# storing the data in 2 files which is completely optional, checked to see which format of file occupies least storage
# Save all data to a JSON file
with open('energy_sources.json', 'w') as json_file:
    json.dump(all_data, json_file, indent=2)

# Convert the list of dictionaries to a Pandas DataFrame
df = pd.DataFrame(all_data)

# Save the DataFrame to a CSV file
df.to_csv('energy_sources.csv', index=False)
