var dee = require("./dee")

dee = dee.create_dee();
dee.worker("/workers/jazz", function(w) { console.log(w) });
dee.send_message("/workers/delicious", "wot");

