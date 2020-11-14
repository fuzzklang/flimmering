# Write JSON-file
# Test

import json

# TODO: GET PROPER PATH!
path = "flimmering/"

json_data = json.JSONEncoder().encode(my_data_structure)

with open ("test.json", mode="w") as doc:
    doc.write(json_data)
