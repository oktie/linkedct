String.prototype.trunc = String.prototype.trunc ||
      function(n){
          return this.length>n ? this.substr(0,n-1)+'&hellip;' : this;
      };

client = {
	init : function(endpointUrl) {
        /*
         * Initialize the server setting
         */
        var srch2ServerSetting = {
            serverUrl : endpointUrl, // use your own server URL
            debug : false, // enable the debug mode which will display debug messages to the console.
                          // IE may not have "console.log" function. If you are using IE, please set it to false.
        };
        srch2.init(srch2ServerSetting);    // Initialize server
        srch2.setSearchType("getAll");     // Set the search type to "getAll"
        srch2.setEnablePrefixSearch(true); // Enable prefix search
        srch2.setEnableFuzzySearch(true);  // Enable fuzzy search
        this.bindInput(); // bind input events to a function
    },
	/*
	* Bind the input box "query_box" key up event with
	* a function which sending the query to the server.
	*/
   bindInput : function() {
	   var element = document.getElementById("search-query");
	   this.bindEvent(element, "keyup", function(event) {
		   if (event.keyCode == 13) {
			   return;
		   }
		   var query = client.sendQuery();
	   });
   },
   /*
     * Bind the event "type" to the HTTP element "element".
     * If the "type" event is triggered, call the function "handler".
     */
    bindEvent : function(element, type, handler) {
        if (element.addEventListener) {
            element.addEventListener(type, handler, false);
        } else {
            element.attachEvent('on' + type, handler);
        }
    },
	/*
     * This function gets the keyword query from the "query_box"
     * and sends the query to the server. The response
     * will trigger the function "this.responseHandler".
     */
    sendQuery : function() {
        var query = document.getElementById('search-query').value;
        srch2.sendQuery(query, this.responseHandler);
    },

    /*
     * "responseHandler" is called after we get the server response.
     * The "responseText" contains all the results in JSON format.
     */
    responseHandler : function(responseText) {
        if (responseText) {
            var output = "";
            var results = responseText.results;
            client.queryKeywords = responseText.query_keywords;
            for (var i = 0; i < results.length; i++) {
                output += "<div class='result-row'>";
                var record = results[i].record;
                var prefix = results[i].matching_prefix;
                output += "<div class='result-title'><a href='/resource/trial/" + record.slug + "/'>" + client.addHighlighting(prefix, record.brief_title) + "</a></div>";
				output += "<div class='result-description'><small>" + client.addHighlighting(prefix, record.detailed_description.trunc(500)) + "</small></div>";
                output += "</div>";
            }
            // client.log("got it", "debug");
            // client.log(JSON.stringify(responseText), "debug");
            var element = document.getElementById("search-result");
            if (output == "") {
                element.innerHTML = "No results mate!";
            } else {
                element.innerHTML = output;
            }
        } else {
            var element = document.getElementById("search-result");
            element.innerHTML = "No results mate!";
            // client.log("empty response", "debug");
        }
    },

    /*
     * Highlight the prefix in the search results.
     */
    addHighlighting : function(prefix, input) {
        if (input) {
            input = input.toString();
            var words = input.split(/[ ]+/);
            // split by space
            var output = "";
            for (var wordIndex in words) {
                var word = words[wordIndex];
                var tempWord = word.toLocaleLowerCase();
                var match = this.regexMatch(prefix, word);
                var space = "";
                if (wordIndex > 0) {
                    space = " ";
                }
                if (match.success) {
                    var first_part = match.first;
                    var second_part = match.second;
                    var classStr = match.class;
                    output += space + "<span class='" + classStr + "'>" + first_part + "</span>" + second_part;
                } else {
                    output += space + word;
                }
            }
            return output;
        }
        return input;
    },
    regexMatch : function(prefixArray, word) {
        var prefixStr = prefixArray.join("|^");
        var re = new RegExp('^' + prefixStr, 'i');
        var m = re.exec(word);
        var returnObj = {};
        if (m == null) {
            // this.log("no match", "debug");
            returnObj.success = false;
            return returnObj;
        } else {
            var first_part = word.substring(0, m[0].length);
            var second_part = word.substring(m[0].length);
            returnObj.success = true;
            returnObj.first = first_part;
            returnObj.second = second_part;
            returnObj.matched = m[0];

            if (this.findPrefix(this.queryKeywords, returnObj.matched)) {
                // exact
                if (word.length == m[0].length) {
                    // exact complete
                    returnObj.class = 'exact_complete';
                } else {
                    // exact prefix
                    returnObj.class = 'exact_prefix';
                }
            } else {
                // fuzzy
                if (word.length == m[0].length) {
                    // fuzzy complete
                    returnObj.class = 'fuzzy_complete';
                } else {
                    // fuzzy prefix
                    returnObj.class = 'fuzzy_prefix';
                }
            }
            return returnObj; facet_remove_filter
        }
    },
    findPrefix : function(keywords, prefix) {
        prefix = prefix.toLocaleLowerCase();
        for (var index in keywords) {
            if (keywords[index].localeCompare(prefix) == 0) {
                return true
            }
        }
        return false;
    },

    log : function(msg, debug) {
        /*
         Handy debug function. Use this function instead of alert or console.log
         */
        if (debug == "debug") {
            console.log(msg);
        }
    },
}
