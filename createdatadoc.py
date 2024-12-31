from openpyxl import Workbook
from merakidata import getMerakiData

switch_downtimes, ap_downtimes = getMerakiData()

# Create an Excel workbook
wb = Workbook()
ws = wb.active
ws.title = "Meraki Data"

# Write data to specific cells
ws["A1"] = "Device Name"
ws["B1"] = "Uptime Percentage"
for i, switch_downtime in enumerate(switch_downtimes, start=2):
    ws[f"A{i}"] = switch_downtime['device_name']
    ws[f"B{i}"] = switch_downtime['uptime_percentage']

# Save the Excel file
file_name = "Meraki_Data.xlsx"
wb.save(file_name)
print(f"Data saved to {file_name}")