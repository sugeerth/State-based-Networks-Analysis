var csv = require('csv-parser')
var fs = require('fs')

fs.createReadStream('../COW_Trade_4.0/Dyadic_COW_4.0.csv')
	.pipe(csv())
	.on('data', function (data) {
		fs.appendFileSync('data.txt', data.ccode2+" "+data.ccode1+" "+data.year+"\n");
	})
