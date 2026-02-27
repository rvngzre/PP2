import json


print("Interface Status")
print("=" * 80)
print(f"{'DN':50} {'Description':20} {'Speed':7} {'MTU':5}")
print("-" * 50 + " " + "-" * 20 + " " + "-" * 7 + " " + "-" * 5)


with open("sample-data.json", "r") as json_file:
    parsed_data = json.load(json_file)

data = parsed_data["imdata"]

for part in data[:3]:
    attr = part["l1PhysIf"]["attributes"]
    
    dn = attr.get("dn", "")
    descr = attr.get("descr", "")
    speed = attr.get("speed", "")
    mtu = attr.get("mtu", "")
    
    print(f"{dn:50} {descr:20} {speed:7} {mtu:5}")