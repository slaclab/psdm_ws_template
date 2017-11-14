var WebSocketConnection = (function(){
    self.connect=function(){
    	// We use the window.location to compute the location of the socket.io endpoint.
    	// To debug connectivity issues, set localStorage.debug = "*" in the Chrome console before loading this page.
    	// Apache configuration; create separate endpoints for the HTTP and socket.io
    	// Send any polling transport socket.io calls to http
    	// RewriteCond %{QUERY_STRING} transport=polling
    	// RewriteRule "^/batch_manager_socketio/(.*)$" http://localhost:5000/$1 [P]
    	// ProxyRequests off
    	// ProxyPass /batch_manager/ http://localhost:5000/
    	// ProxyPass /batch_manager_socketio/socket.io/ ws://localhost:5000/socket.io/
    	// ProxyPassReverse /batch_manager_socketio/socket.io/ ws://localhost:5000/socket.io/

    	var namespace = '/psdm_ws';
    	var sockIoPath = app_root_path + "_socketio/socket.io/"; // The final trailing slash is very important....
    	var scheme = (window.location.protocol == "http:") ? "ws" : "wss";
        console.log("Connecting to socketIO using " + sockIoPath + " using " + scheme);
        var socket = io.connect(scheme + "://" + document.domain + ':' + location.port + namespace, { transports : ['websocket'], 'path': sockIoPath });
        socket.on('connect',function(){
            console.log('Websocket connected to URL' + sockIoPath);
            socket.emit('join',experiment_name);
            console.log("Joined room",experiment_name);
        });
    
        socket.on('connect_error',function(err){
            console.log('Websocket failed to connect to URL');
            console.log(err);
        });
    
        socket.on('disconnect',function(){
            console.log('Disconnecting from websockets at ', sockIoPath);
        });
    
        socket.on('update_job_status',function(update_msg){
            console.log("update_job_status",update_msg);
            update_msg["storedHashes"] = HashCache.storedHashes;
            Updater.update_job_status(update_msg);
        });    

        socket.on('status_answer',function(status_msg){
            console.log(status_msg);
            Updater.initialize(status_msg);
        });  

        socket.on('update_run_group_status',function(update_msg){
            console.log("update_run_group_status",update_msg);
        });    

        socket.on('ping', function(resp){
            console.log(resp);
        })
       
    };

    return self;
})();
