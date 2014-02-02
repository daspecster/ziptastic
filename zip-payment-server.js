var stripe = require("stripe")(
  "sk_test_oVnxvM8zkSBZhN7NAWk7uQWF"
), http = require('http'),
qs = require('querystring');

http.createServer(function (request, res) {
    res.writeHead(200, {'Content-Type': 'text/plain'});

    console.log(request.method);

    requestBody = "";

    request.on('data', function(data) {
          requestBody += data;
    });

    request.on('end', function() {
      var formData = qs.parse(requestBody);
      console.log(formData);
    });
    // stripe.customers.create({
    //   description: 'Customer for test@example.com',
    //   email: "daspecster@gmail.com",
    //   card: "tok_102y0F2nRtMq07bxFTa9FUb1",
    //   plan: "small",
    //   metadata: {domain: "example.com"}
    // }, function(err, customer) {
    //   // asynchronously called
    // });
    res.end('Hello World\n');

}).listen(1337, '127.0.0.1');
console.log('Server running at http://127.0.0.1:1337/');

