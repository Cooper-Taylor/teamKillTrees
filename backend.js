//Notes: in future put backend stuff in own folder and maybe separate node modules for frontend and backend

const express = require('express');
const app = express();
app.disable('x-powered-by'); //helps for opsec
const http = require('http');
const server = http.createServer(app);
const { Server } = require('socket.io');
const io = new Server(server);
const crypto = require('crypto');

let data;

//Communication stuff
app.get('/', (req, res) => { 
    res.sendFile(__dirname + '/frontend/index.html');



});

//app.use('/static', express.static(__dirname + '/' ) ); 
app.use(express.static(__dirname + '/frontend' ) );

let runPy = new Promise(function(success, nosuccess) {

    const { spawn } = require('child_process');
    const pyprog = spawn('python', ["../flightDataTracker.py"]);

    pyprog.stdout.on('data', function(res) {
        data = res;
        //console.error(data.toString())
    });

    pyprog.stderr.on('data', (res) => {
        data = res;
        //console.error(data.toString())
    });
});

runPy.catch((error) => {
    console.error(error.toString());
})

io.on('connection', (socket) => {
    socket.emit("hello", "hello world!"); //"hello" is the event name and "hello world" is the message or data sent for that event
    
    runPy.then(function(output) {
        console.log(data.toString());
        console.error(data.toString());
        socket.emit("update", data)
    })

    socket.on("update", (data, callback)=>{
        
    });

     //"hello" is the event name and "hello world" is the message or data sent for that event

});


//get server ready to serve files
server.listen(process.env.PORT || 3001, () => {});


