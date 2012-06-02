var util = require("util");
var events = require("events");
var redis = require("redis");
var net = require("net");

function DistEventEmitter(sub_stream, pub_stream, options) {
    this._id = "node:" + process.pid;
    this._publisher = new redis.RedisClient(pub_stream, options);
    redis.RedisClient.call(this, sub_stream, options); 
}

util.inherits(DistEventEmitter, redis.RedisClient);

DistEventEmitter.prototype._dispatcher = function (channel, data) {
    msg = JSON.parse(data.toString('utf8'));                                    
    evt = msg.properties.delivery_info.routing_key                              
    d = new Buffer(msg.body, 'base64').toString()                               
    this.emit(evt, d);                                                               
} 

DistEventEmitter.prototype.send_message = function(worker, message) {
    pkt = JSON.stringify({ "_id": this._id, "message": message});
    p_b64 = new Buffer(pkt).toString("base64");
    env = {"body": p_b64, "headers": {}, "content-type": "application/data", 
           "properties": {"body_encoding": "base64", "delivery_info": 
               {"priority": 0, "routing_key": worker, "exchange": "exchange:"+worker}, 
            "delivery_mode": 2, "delivery_tag": 1 }, 
           "content-encoding": "binary"};
    this._publisher.publish("exchange:"+worker, JSON.stringify(env))
}

DistEventEmitter.prototype.worker = function(workername, fun) {
    this.subscribe("exchange:"+workername);
    this.on(workername, fun);
}

exports.create_dee = function (host, port, options) {                 
    var port = port || 6379,
        host = host || "127.0.0.1",
        dee_client, net_client;                                               
    sub_client = net.createConnection(port, host);                              
    pub_client = net.createConnection(port, host);                              
    _dee = new DistEventEmitter(sub_client, pub_client, options);
    _dee.on("message", _dee._dispatcher);
    _dee.on("error", function(err){ console.log("DEE client error " + err); });
    return _dee;                                                        
};

