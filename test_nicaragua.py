import json

# Last inn landdata
with open('countries_data.json', 'r', encoding='utf-8') as f:
    countries_data = json.load(f)

# Finn Nicaragua
nicaragua = None
for country in countries_data:
    if country['name'] == 'Nicaragua':
        nicaragua = country
        break

if nicaragua:
    print(f"Nicaragua funnet:")
    print(f"  Name: {nicaragua['name']}")
    print(f"  ISO3: {nicaragua['iso3']}")
    print(f"  flagFile: {nicaragua.get('flagFile', 'MANGEL')}")
else:
    print("Nicaragua ikke funnet!")

# Sjekk hvor mange som har flagFile
with_flag = sum(1 for c in countries_data if c.get('flagFile'))
without_flag = sum(1 for c in countries_data if not c.get('flagFile'))

print(f"\nTotalt:")
print(f"  Med flagg: {with_flag}")
print(f"  Uten flagg: {without_flag}")
print(f"  Totalt: {len(countries_data)}")
