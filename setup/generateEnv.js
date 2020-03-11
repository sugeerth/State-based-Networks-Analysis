//Parser to generate .env file

var path = require("path");
var rootdir = path.resolve(__dirname, '..')+'/';

var env = process.env.NODE_ENV || "DEVELOPMENT"

var configurations = require("./config.js")

var fs = require('fs');
var stream = fs.createWriteStream(rootdir+".env", {'flags': 'w'});
stream.once('open', function() {
	stream.write("ROOTDIR="+rootdir+"\n");

	Object.keys(configurations).forEach(function(config) {
		stream.write(config+"="+configurations[config]);
	})
	stream.end();
});
