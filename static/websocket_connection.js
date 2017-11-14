var WebSocketConnection = (function(){
    self.connect=function(){
    	// We use the window.location to compute the location of the socket.io endpoint.
    	// To debug connectivity issues, set localStorage.debug = "*" in the Chrome console before loading this page.
    	// Apache configuration; create separate endpoints for the HTTP and socket.io
    	//    	<LocationMatch "^/psdm_socketio/(.*)$">
    	//    	  RequestHeader set REMOTE_USER %{WEBAUTH_USER}e
    	//    	  ProxyPass ws://localhost:5000/$1
    	//    	  ProxyPassReverse ws://localhost:5000/$1
    	//    	</LocationMatch>

    	var namespace = '/psdm_ws';
    	// Make an assumption that the application is hosted one level down in the web server namespace.
    	var appRootPath = window.location.pathname.split("/").slice(0,2).join("/")
    	if (typeof app_root_path != 'undefined') {
    		console.log("Overriding the socketio root path with app_root_path " + app_root_path);
    		appRootPath = app_root_path;
    	}
    	var sockIoPath = appRootPath + "_socketio/socket.io/"; // The final trailing slash is very important....
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
