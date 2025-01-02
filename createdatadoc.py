from openpyxl import Workbook
from merakidata import getMerakiData

switch_downtimes, ap_downtimes = getMerakiData()

# Create an Excel workbook
wb = Workbook()
ws = wb.active
ws.title = "Meraki Data"

# Write data to specific cells
row = 1
ws[f"A{row}"] = "Device Name"
ws[f"B{row}"] = "Uptime Percentage"
for i, switch_downtime in enumerate(switch_downtimes, start=row+1):
    ws[f"A{i}"] = switch_downtime['device_name']
    ws[f"B{i}"] = switch_downtime['uptime_percentage']
    row = i

for i, ap_downtime in enumerate(ap_downtimes, start=row+2):
    ws[f"A{i}"] = ap_downtime['device_name']
    ws[f"B{i}"] = ap_downtime['uptime_percentage']
    row = i

# Save the Excel file
file_name = "Meraki_Data.xlsx"
wb.save(file_name)
print(f"Data saved to {file_name}")