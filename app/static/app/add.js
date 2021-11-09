
var parent = document.getElementsByClassName("content container-fluid")[0];
var contain = document.createElement("div");
contain.setAttribute("class", "contain");

var section = document.createElement("section");
section.setAttribute("class", "section");



var row = document.createElement("div");
row.setAttribute("class", "row");;

var col_xs_12 = document.createElement("div");
col_xs_12.setAttribute("class", "col-xs-12");

var box = document.createElement("div");
box.setAttribute("class", "box");

var box_body = document.createElement("div");
box_body.setAttribute("class", "box-body table-responsive no-padding");

var table = document.createElement("table");
table.setAttribute("class", "table table-hover");
table.setAttribute("id", "userTable");

var thead = document.createElement("thead");


var tr = document.createElement("tr");



var th_text = ["diuwebd", "euudwe", "eiwubd"];
for (var i = 0; i < th_text.length(); i++) {
    var th = document.createElement("th");
    var node = document.createTextNode(th_text[i])
    th.appendChild(node);
    tr.appendChild(th);
}

thead.appendChild(tr);


// start loop
var tbody = document.createElement("tbody");
var tr = document.createElement("tr");
var td = document.createElement("td");
var node = document.createTextNode("lalala");
td.appendChild(node);
tr.appendChild(td);


var tbody = document.createElement("tbody");
var tr = document.createElement("tr");
var td = document.createElement("td");
var node = document.createTextNode("lalala");
td.appendChild(node);
tr.appendChild(td);


var tbody = document.createElement("tbody");
var tr = document.createElement("tr");
var td = document.createElement("td");
var node = document.createTextNode("lalala");
td.appendChild(node);
tr.appendChild(td);


var tbody = document.createElement("tbody");
var tr = document.createElement("tr");
var td = document.createElement("td");
var node = document.createTextNode("lalala");
td.appendChild(node);
tr.appendChild(td);

// stop loop

tbody.appendChild(tr);

table.appendChild(thead);
table.appendChild(tbody);
box_body.appendChild(table);
box.appendChild(box_body);
col_xs_12.appendChild(box);
row.appendChild(col_xs_12);
section.appendChild(row);
contain.appendChild(section);
parent.appendChild(contain);



