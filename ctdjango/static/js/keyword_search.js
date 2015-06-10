var page = 0;
var fuzzy = 1;
var m = 20;
var busy = false;
var pending = false;
var old_q = "";
var old_fuzzy = 1;
var old_page = 0;

function check(value) {

	page=0;
	hideError();
	var regex=/\+|\s/gi;
	if (value.length==0)
	{
		busy = false;
		document.getElementById('results').innerHTML="";
		document.getElementById('pagination').innerHTML="";
	}
	else if(value.replace(regex,"").length >= 3){
		if(busy)pending = true;
		else query(value);
	}
}

function query(value) {
	var regex=/\+/gi;
	value = value.replace(regex,"");
	value = value.replace(/ +(?= )/g,'');
	var valuestmp = value.split(' ');
	var values = valuestmp;

	for (var i = 0; i < valuestmp.length; i++ )
	{
		if (valuestmp[i]=="")
		values.splice(i,i+1);
	}
	
	var url = "/keyword_search/search?q="
	var first = 1;
	var q = "";
	for(var i = 0; i < values.length; i++) {
		if(values[i]!=''){
    		if(!first)q += "+";
    		q += values[i].toLowerCase();
			first = 0;
		}
	}
	url += q; 
	// if any option's value changes
	if( q != old_q || fuzzy != old_fuzzy || page != old_page ){
		if(fuzzy == 1)
			url += "&fuzzy=1";
		else{
			url += "&fuzzy=0";
		}
			
		url += "&start=" + page*m + "&limit=" + (page+1)*m;
		
		busy = true;
		self.scrollTo(0, 0);
		url += "&jsoncallback=?";
		$.getJSON(url,
		  function (data) {
		    display(data);
		  });
		old_q = q;
		old_fuzzy = fuzzy;
		old_page = page;
	}

}

function display(response) {
	busy = false;
	var trials = response.trials;
    var content = response.content;
	var html = "";
	var indent = "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp";
	
	for (var i = 0; i < trials.length; i++) {
		html += "<hr>";
		html += "<a style='font-size: 150%;' href=../resource/trial/" + trials[i] + ">" + trials[i] + "</a><br>";
		html += "<h3> Title: " + content[trials[i]][0] + "<br> Lead Sponsor: " + content[trials[i]][1] + 
				"<br> Conditions: " + content[trials[i]][2] + "<br> Locations: ";
				
		for (var j = 0; j < content[trials[i]][3].length; j++) {
			if (j == content[trials[i]][3].length - 1) {
				html += content[trials[i]][3][j][0] + " (" + content[trials[i]][3][j][1] + ")";
			} else {
				html += content[trials[i]][3][j][0] + " (" + content[trials[i]][3][j][1] + ")<br>" + indent;
			}
		}
		
		if (content[trials[i]][4] == "1") {
			html += "<br>" + indent + "For more locations see <a href=../resource/trial/" + trials[i] + "> the trial page</a>.";		
		}
		
		html += "</h3>";
	}
	

	document.getElementById('results').innerHTML=html;

	html = "";

	if(page) 
		html += "<a style='text-decoration: none;' href='#' onclick='goToFirstPage()'>&#171;&#160;First</a> "
		+ "&nbsp;&nbsp;<a style='text-decoration: none;' href='#' onclick='goToPreviousPage()'>Previous</a> "
		+ "&nbsp;&nbsp;<a href='#' onclick='goToPreviousPage()'>" + page + "</a> &nbsp;|&nbsp;";

	if(page || trials.length >= m)
		html += (page+1);

	if(trials.length >= m)
		html += "&nbsp;|&nbsp;<a href='#' onclick='goToNextPage()'>" + (page+2) + "</a>&nbsp;&nbsp;"
		+ "<a style='text-decoration: none;' href='#' onclick='goToNextPage()'>Next</a>";
       
	document.getElementById('pagination').innerHTML = html;

	if(pending) {
		pending = false;
		query(document.getElementById('input').value);
	}

}

function goToFirstPage(){
	page=0;
	query(document.getElementById('input').value);
	return false;
}

function goToPreviousPage(){
	page--;
	query(document.getElementById('input').value);
	return false;
}

function goToNextPage(){
	page++;
	query(document.getElementById('input').value);
	return false;
}

function prepareRegex(keys, ed) {
	var regex1 = "([^A-Za-z0-9_&])(";
	var regex2 = "([^A-Za-z0-9_&])(";
	var j1 = 0;
	var j2 = 0;
	for(var k = 0; k < keys.length; k++)
	if(keys[k].length)
		if(ed[k] == 0) {
		if(j1)regex1 += "|";
		regex1 += keys[k].replace(/\W/g, 
		    function(sub){return "\\" + sub;});
		j1++;
		}
		else {
		if(j2)regex2 += "|";
		regex2 += keys[k].replace(/\W/g, 
		    function(sub){return "\\" + sub;});
		j2++;
		}

	regex1 += ")";
	regex2 += ")";
	return [ (j1)?new RegExp(regex1, "gi"):null, (j2)?new RegExp(regex2, "gi"):null ];
}

function highlight(string, regexp, stylec1, stylec2) {
	var str = " " + string.replace(/</g, "&lt;");
	if(regexp == null)
		return str;
	if(regexp[0] != null)
		str = str.replace(regexp[0], function(sub, m1, m2) {
			return m1 + "<span class='" + stylec1 + "'>" + m2 + "</span>";
		    });
	if(regexp[1] != null)
	    str = str.replace(regexp[1], function(sub, m1, m2) {
	    return m1 + "<span class='" + stylec2 + "'>" + m2 + "</span>";
	});
	return str.replace(/^\s+/, '');;
}

function enableLink(linkid,textid) {
	var link=document.getElementById(linkid);
	var text=document.getElementById(textid);
	text.style.display="none";
	link.style.display="";
}
function disableLink(linkid, textid) {
	var link=document.getElementById(linkid);
	var text=document.getElementById(textid);
	link.style.display="none";
	text.style.display="";

}

function displayError(txt){
	var err = document.getElementById( 'errorMsg' );
	err.style.display="";
	err.innerHTML = txt;
}

function hideError(){
	var err = document.getElementById( 'errorMsg' );
	err.style.display="none";
}

function clickOn(){
	fuzzy=1;
	check(document.getElementById('input').value);
	disableLink('on','onText');
	enableLink('off','offText');
}

function clickOff(){
	fuzzy=0;
	check(document.getElementById('input').value);
	disableLink('off','offText');
	enableLink('on','onText');
}
