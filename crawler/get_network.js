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
    // setup handlers
    Network.requestWillBeSent((params) => {
        console.log(params.request.url);
    });
    Page.loadEventFired(() => {
        setTimeout(function(){
           const id = client.target.id;
           CDP.Close({id});
           client.close();
         }, 30000);
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

