import xml.etree.ElementTree as ET
import keyring

xml_path = "/home/uber/Desktop/fuck.xml"
service_name = "AES"  # The service AES uses to store secrets

tree = ET.parse(xml_path)
root = tree.getroot()

count = 0
for pw in root.findall(".//password"):
    name = pw.get("name")
    value = pw.text
    if not name or not value:
        continue
    keyring.set_password(service_name, name, value)
    print(f"✅ Imported: {name}")
    count += 1

print(f"\n✅ Done — imported {count} secrets into {keyring.get_keyring()}")
