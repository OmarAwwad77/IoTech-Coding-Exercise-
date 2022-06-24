import argparse
import json
import re


parser = argparse.ArgumentParser(description='Reformat Json Files')

parser.add_argument('-f', '--filePath', required=True, type=str, metavar='', help='path of the json file to be formatted')
parser.add_argument('-i', '--indent', type=int, metavar='', help='indentation of the new formatted json file', default=2)

args = parser.parse_args()

file = open(args.filePath)
content = json.load(file)
devices = content['Devices']

for device in devices:
  new_fields = {}

  for key, val in device.items():
    if key == 'Info':
      match_object = re.search(':.+,', val)
      if match_object:
        start_ind, end_ind = match_object.span()
        new_fields['uuid'] = val[start_ind+1:end_ind-1]

    if key == 'Sensors':
      total_payload = 0
      for sensor in val:
        total_payload += sensor['Payload']
      new_fields['PayloadTotal'] = total_payload

  device.update(new_fields)
  del device['Sensors']

devices.sort(key= lambda device: device['Name'].lower())

formatted_file = open('solution.json', 'w')
json.dump({'Devices': devices}, formatted_file, indent=args.indent)
formatted_file.close()