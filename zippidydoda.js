(function( $ ) {
  $.fn.ziptastic = function( options ) {
  	
    // Create some defaults, extending them with any options that were provided
    var settings = $.extend( {
      'zip' 	  : 'zip',	
      'cityid'    : 'city',
      'stateid'   : 'state',
      'countryid' : 'country'
    }, options);	

    return this.each(function() {        
    	var zip_element = this.children("#" + settings.zipid);
		var city_element = this.children("#" + settings.cityid);
		var state_element = this.children("#" + settings.stateid);
		var country_element = this.children("#" + settings.countryid);

		// Hide the elements that we're going to retreive data for.
		city_element.hide();
		state_element.hide();
		country_element.hide();

		//TODO: Capture the onchange event of the zip field...

	    var client = new XMLHttpRequest();
		client.open("GET", "http://localhost?zip=48867", true);
		client.onreadystatechange = function() {
			if(client.readyState == 4) {
				alert(client.responseText);
				var location_data = this.parseJSON(client.responseText);

				city_element.val(location_data[0]);
				state_element.val(location_data[1]);
				country_element.val(location_data[2]);
		  	};
		};
		  
		client.send();

    });

  };
})( jQuery );