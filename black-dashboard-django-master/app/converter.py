import csv
def convert(name1):
	name = name1.replace(" ", "").lower()
	with open('tickernames.csv', 'r') as file:
		tickers = csv.reader(file, delimiter = ',')
		for rows in tickers:
			# print(rows[1])
			if rows[1].replace(" ", "").lower() == name:
				return rows[0]

# print(convert("ZynerbaPharmaceuticals"))