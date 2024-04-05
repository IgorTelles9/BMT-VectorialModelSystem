#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 18:36:27 2024

@author: igort
"""

# ler o arquivo de entrada 


from xml.etree import ElementTree as ET

def parse_xml_file(filename):
  data = {}
  try:
    tree = ET.parse(filename)
    root = tree.getroot()

    # Extract information from top level tags
    data["QueryNumber"] = root.find("QUERY/QueryNumber").text
    data["QueryText"] = root.find("QUERY/QueryText").text
    data["Results"] = root.find("QUERY/Results").text

    # Extract data from Item tags
    items = []
    for item in root.findall("QUERY/Records/Item"):
      item_data = {
          "score": item.get("score"),
          "number": item.text
      }
      items.append(item_data)
    data["Items"] = items

    return data
  except FileNotFoundError:
    print("Error: File not found!")
    return {}

# Example usage
filename = "your_file.xml"  # Replace with your actual filename
data = parse_xml_file(filename)

if data:
  print("Query Number:", data["QueryNumber"])
  print("Query Text:", data["QueryText"])
  print("Results:", data["Results"])
  print("\nItems:")
  for item in data["Items"]:
    print(f"  Score: {item['score']}, Number: {item['number']}")
else:
  print("No data found in the file.")
