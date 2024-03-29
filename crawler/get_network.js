const CDP = require('chrome-remote-interface');

var url_string;
process.argv.forEach(function (val, index, array) {
    if(index === 2) {
        url_string = val;
    }
});

CDP((client) => {
    // extract domains
    const {Network, Page} = client;
    const id = client.target.id;
    // setup handlers
    Network.requestWillBeSent((params) => {
        console.log(params.request.url);
    });
    Page.loadEventFired(() => {
        setTimeout(function(){
           console.log("TAB_ID_IS: " + id);
           //CDP.Close({id});
           client.close();
         }, 4000);
    });
    // enable events then start!
    Promise.all([
        Network.enable(),
        Page.enable()
    ]).then(() => {
        return Page.navigate({url: url_string});
    }).catch((err) => {
        console.error(`ERROR: ${err.message}`);
        client.close();
    });
}).on('error', (err) => {
    console.error('Cannot connect to remote endpoint:', err);
});

