import csv
from datetime import datetime
import string
'''
You will also find that a project may not show 'complete' in the application status (col B) but has a PV meter install date (col OF). If there is a date it is complete.  However if there is no date and status is complete, that is also complete. 
'''
with open("smud_solar_oct_2014.csv", 'rU') as f, open('SMUDclean.csv', 'wb') as new_csv:
	outfields = ['Application Number', 'Current Application Status','First Completed Date','PV Meter Installed Date', 'Program', 'Utility', 'Incentive Amount', 'Total System Cost', 'Incentive Design Description', 'Incentive Design Type', 'Incentive Design Step', 'Incentive Design Rate', 'Incentive Design Step (kW)', 'Incentive Design Rate (kW)', 'Installation Costs #1 Manufacturer', 'Installation Costs #1 Model', 'Installation Costs #1 Quantity', 'Installation Costs #1 Cost', 'Cost/CEC PTC Watt Before Incentive', 'Cost/CEC PTC Watt After Incentive', 'Nameplate Rating (KW)', 'CEC PTC Rating (KW)', 'CSI Rating (KW)', 'Design Factor', 'Estimated Production Actual (KWH)', 'PV Module #1 Manufacturer', 'PV Module #1 Model', 'PV Module #1 Quantity', 'PV Module #1 Cost', 'PV Module #1 PTC Rating', 'PV Module #1 Azimuth', 'PV Module #1 Tilt', 'PV Module #1 Tracking', 'PV Module #2 Manufacturer', 'PV Module #2 Model', 'PV Module #2 Quantity', 'PV Module #2 Cost', 'PV Module #2 PTC Rating', 'PV Module #2 Azimuth', 'PV Module #2 Tilt', 'PV Module #2 Tracking', 'PV Module #3 Manufacturer', 'PV Module #3 Model', 'PV Module #3 Quantity', 'PV Module #3 Cost', 'PV Module #3 PTC Rating', 'PV Module #3 Azimuth', 'PV Module #3 Tilt', 'PV Module #3 Tracking', 'Inverter #1 Manufacturer', 'Inverter #1 Model', 'Inverter #1 Quantity', 'Inverter #1 Cost', 'Inverter #1 Efficiency', 'Inverter #2 Manufacturer', 'Inverter #2 Model', 'Inverter #2 Quantity', 'Inverter #2 Cost', 'Inverter #2 Efficiency', 'Annual Electric Usage', 'Inspection Notes', 'Building Type', 'Building Square Footage', 'Building_Type', 'DG Number', 'SMUD Owned System', 'Applicant First Name', 'Applicant Last Name', 'Applicant Company', 'Host Customer Sector', 'Host Customer Subsector', 'Host Customer Physical Address Line 1', 'Host Customer Physical Address Line 2', 'Host Customer Physical Address City', 'Host Customer Physical Address County', 'Host Customer Physical Address State', 'Host Customer Physical Address Zip Code', 'Host Customer Physical Address Zip Code Suffix', 'Installer Company', 'System Owner Company', 'System Owner Is 3rd Party Owner']


	solardata = csv.DictReader(f)
	fields = list(solardata.fieldnames)
	count = 0
	sizes = ["less2", "from2to5", "from5to10", "morethan10"]
	sizedict = {k: [] for k in sizes}
	def reduce(line,array):
		newline = {}
		for item in array:
			newline[item] = line[item]
		return newline

	def sort_by(n,sort_by):
		newdict = sorted(n, key = lambda k: k[sort_by])
		return newdict
	for line in solardata:
		line = reduce(line, outfields)
		if line["PV Meter Installed Date"] or (line["Current Application Status"]).lower() == "completed":
			if not line["PV Meter Installed Date"]:
				line["PV Meter Installed Date"] = line["First Completed Date"]
			try:
				line["PV Meter Installed Date"] = datetime.strptime(line["PV Meter Installed Date"], "%m/%d/%y")
			except:
				line["PV Meter Installed Date"] = datetime.strptime(line["PV Meter Installed Date"], "%d-%b-%y")
			if line["Program"] == "Residential Retrofit PV Program":
				line["Nameplate Rating (KW)"] = float(line["Nameplate Rating (KW)"])
				if line["Nameplate Rating (KW)"] < 2:
					sizedict["less2"].append(line)
				elif line["Nameplate Rating (KW)"] < 5:
					sizedict["from2to5"].append(line)
				elif line["Nameplate Rating (KW)"] < 10:
					sizedict["from5to10"].append(line)
				else:
					sizedict["morethan10"].append(line)
	monthlisting = {}
	#sizedict format is: {size: {month:price, },}
	for size in sizedict:
		monthlisting[size] = {}
		for line in sizedict[size]:
			month = line["PV Meter Installed Date"].strftime("%Y/%m")
			kw = line["Nameplate Rating (KW)"]
			cost = float(line["Total System Cost"])
			if month not in monthlisting[size]:
				monthlisting[size][month] = [kw,cost]
			else:
				monthlisting[size][month][0] += kw
				monthlisting[size][month][1] += cost
	for size in monthlisting:
		for date in monthlisting[size]:
			totals = monthlisting[size][date]
			monthlisting[size][date] = totals[1]/totals[0]
	# current format: monthlisting{size{month:amount,}}
	# need dict with fields as: {date: date, less2: less2, from2to5: from2to5, from5to10: from5to10, morethan10: morethan10}
	all_months = []
	for size in monthlisting:
		for month in monthlisting[size]:
			all_months.append(month)
	months = sorted(list(set(all_months)))
	fields = ["date", "less2", "from2to5", "from5to10", "morethan10"]
	writedict = {}
	for month in months:
		writedict[month] = {"date":month}
	for size in monthlisting:
		for month in writedict:
			try: 
				if monthlisting[size][month]:
					writedict[month][size] = monthlisting[size][month]
				else:
					writedict[month][size] = 0
			except:
				writedict[month][size] = 0
	print writedict
	writer = csv.DictWriter(new_csv, fields, extrasaction='ignore')
	writer.writeheader()
	for month in months:
		writer.writerow(writedict[month])


		




