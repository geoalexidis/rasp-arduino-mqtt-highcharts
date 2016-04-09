/**
 * Simple connect to a broker and a topic
 * Make sure to npm install mqtt first
 * Start with node get.js
 */
var mqtt    = require('mqtt');
var client  = mqtt.connect('mqtt://broker.mqttdashboard.com');
// var msg = 300;

client.on('connect', function () {
  client.subscribe('paho/test/cp2swag/value'); // subscribe to topic
  // client.publish('presence', 'Hello mqtt'); // possible to publish
});

client.on('message', function (topic, message) {
  // message is Buffer
   console.log(message.toString());
  // msg = message.toString();
  // client.end(); // Closes client
});

// module.exports = msg; // Possbile to export
