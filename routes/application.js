var fs = require('fs');
var express = require('express');
var router  = express.Router();
var PythonShell = require('python-shell');


router.get('/',function(req, res) {
	PythonShell.run('pythonUtils/main.py', {}, function (err, data) {
		if(err)
			console.log(err)

		res.render(process.env.ROOTDIR+ 'views/pages/index.ejs', {"brainDataNetwork": data[1], 
																	"maxTimeSteps":data[0], 
																	"differenceData":data[2],
																	"summaryData": data[3],
																	"states": data[4],
																	"positions": data[5],
																	"labels": data[6]});
	});
});

router.get('/hello',function(req, res) {
	res.send("there")
});

// * must be the last route
router.get('*', function(req, res) {
    res.render(process.env.ROOTDIR+ 'views/pages/index.ejs');
});

module.exports = router;