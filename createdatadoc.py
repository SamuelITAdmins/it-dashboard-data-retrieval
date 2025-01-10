from openpyxl import Workbook
from merakidata import getMerakiData

switch_downtimes, ap_downtimes = getMerakiData()

# Create an Excel workbook
wb = Workbook()
switches_ws = wb.active
switches_ws.title = "Meraki Switches"

# Write data to specific cells
switches_ws["A1"] = "Switches"
switches_ws["B1"] = "Location"
switches_ws["C1"] = "Uptime"
switches_ws["D1"] = "Status"
for i, switch_downtime in enumerate(switch_downtimes, start=2):
    switches_ws[f"A{i}"] = switch_downtime['device_name']
    switches_ws[f"B{i}"] = switch_downtime['location']
    switches_ws[f"C{i}"] = switch_downtime['uptime_percentage']
    switches_ws[f"D{i}"] = switch_downtime['status']

ap_ws = wb.create_sheet(title="Meraki AP")

ap_ws["A1"] = "Access Points"
ap_ws["B1"] = "Location"
ap_ws["C1"] = "Uptime"
ap_ws["D1"] = "Status"
for i, ap_downtime in enumerate(ap_downtimes, start=2):
    ap_ws[f"A{i}"] = ap_downtime['device_name']
    ap_ws[f"B{i}"] = ap_downtime['location']
    ap_ws[f"C{i}"] = ap_downtime['uptime_percentage']
    ap_ws[f"D{i}"] = ap_downtime['status']

# Save the Excel file
file_name = "Meraki_Data.xlsx"
wb.save(file_name)
print(f"Data saved to {file_name}")