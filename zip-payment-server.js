var express = require('express');
var app = express();

var stripe = require("stripe")("sk_test_oVnxvM8zkSBZhN7NAWk7uQWF");



var express = require('express');
var app = express();

app.post('/subscribe', function(req, res){

    // (Assuming you're using express - expressjs.com)
    // Get the credit card details submitted by the form
    // var stripeToken = request.body.stripeToken;

    var stripeToken = "tok_102y0F2nRtMq07bxFTa9FUb1";

    stripe.customers.create({
      description: 'Customer for test@example.com',
      email: "daspecster@gmail.com",
      card: stripeToken,
      plan: "small",
      metadata: {domain: "example.com"}
    }, function(err, customer) {
      // asynchronously called
      console.log(err, customer);
    });

});

app.get('/check/:id', function(req, res){

});

app.listen(1337);
