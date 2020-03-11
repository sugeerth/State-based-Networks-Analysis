#!/bin/env node

var express = require('express');
var bodyParser = require('body-parser')
var favicon = require('serve-favicon');

var TimeSum = function() {

    var self = this;
   
    self.setupVariables = function() {
        //set the environment variables
        self.ipaddress = "127.0.0.1"
        self.port      = 8088;
    };

    self.terminator = function(sig){
        if (typeof sig === "string") {
        console.log('%s: Received %s - terminating TimeSum app ...',
        Date(Date.now()), sig);
        process.exit(1);
    }
    console.log('%s: Node server stopped.', Date(Date.now()) );
 };


    //setup termination handlers (for exit and a list of signals)
    self.setupTerminationHandlers = function(){
        //process on exit and signals
        process.on('exit', function() { self.terminator(); });

        // Removed 'SIGPIPE' from the list - bugz 852598.
        ['SIGHUP', 'SIGINT', 'SIGQUIT', 'SIGILL', 'SIGTRAP', 'SIGABRT', 'SIGBUS', 
        'SIGFPE', 'SIGUSR1', 'SIGSEGV', 'SIGUSR2', 'SIGTERM']
        .forEach(function(element) {
            process.on(element, function() { self.terminator(element); });
        });
    };


    self.createRoutes = function() {
        var routes = require("./routes/application")
        self.routes = routes;
    };

    //initialize the server (express) and create the routes and register the handlers
    self.initializeServer = function() {
        self.createRoutes();
        self.app = express();
        self.app.use(favicon('public/images/timesum.png'))
        self.app.use(bodyParser.json())
        self.app.use(bodyParser.urlencoded({extended: false}));
        self.app.use(express.static( "public"));
        self.app.use('/',self.routes)
    };


    //initializes the sample application
    self.initialize = function() {
        self.setupVariables();
        self.setupTerminationHandlers();

        // create the express server and routes
        self.initializeServer();
    };


    //start the server (starts up the application)
    self.start = function() {
        self.app.listen(self.port, self.ipaddress, function() {
            console.log('%s: Node server started on %s:%d ...',Date(Date.now() ), self.ipaddress, self.port);
        });
    };

};


var zapp = new TimeSum();
zapp.initialize();
zapp.start();

