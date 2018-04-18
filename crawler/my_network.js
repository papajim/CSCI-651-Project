const CDP = require('chrome-remote-interface');

var url_string;
process.argv.forEach(function (val, index, array) {
    if(index === 2) {
        url_string = val;
    }
});

//CDP().on('error', (err) => {
//   console.error('Cannot connect to remote endpoint:', err);
//});

CDP.New().then((target) => {
   return CDP({target});
}).then((client) => {
    // extract domains
    const {Network, Page} = client;
    // get tab id
    const id = client.target.id;
    // setup handlers
    Network.requestWillBeSent((params) => {
        console.log(params.request.url);
    });
    Page.loadEventFired(() => {
        setTimeout(function(){
           CDP.Close({id});
           client.close();
         }, 40000);
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
});

