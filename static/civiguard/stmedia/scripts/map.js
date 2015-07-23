var addState = "none";
var localeArr = [];
var localeGeoArr = [];
var poiArr = [];
var poiGeoArr = [];
var map;
var lMarkers = [];
var pMarkers = [];
var infoWindow = [];
var geocoder;
var selectedMarker;
var selecterMarkerType;

function initialize() {
    geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(30.340763, -97.556946);
    var myOptions = {
        zoom: 15,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        mapTypeControl: true,
        mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
            position: google.maps.ControlPosition.TOP_RIGHT
        },
        navigationControl: true,
        navigationControlOptions: {
            style: google.maps.NavigationControlStyle.ZOOM_PAN,
            position: google.maps.ControlPosition.RIGHT
        }
    };
    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

    $('#message').glow('green', 2000, 400);
}

function addLocaleAction(){
    if(localeArr.length<2){
        addState = "locale";
        setMessage("Drag the marker to the location", "ins");
        placeMarker(map.getCenter());
        return;
    }
    if(localeArr.length==2){
        setMessage("You can add only upto 2 locales", "error");
    }
}


function addPoiAction(){
    if(poiArr.length<10){
        addState = "poi";
        setMessage("Drag the marker to the location", "ins");
        placeMarker(map.getCenter());
        return;
    }
    if(poiArr.length==10){
        setMessage("You can add only upto 10 points", "error");
    }
}

function placeMarker(location) {
    if(addState=="locale"){
        var clickedLocation = new google.maps.LatLng(location);
        var marker = new google.maps.Marker({
            position: location,
            map: map,
            shadow: lShadow,
            icon: aniImage,
            shape: lShape

        });
        //add the marker to array
        localeArr.push(marker);
        document.getElementById("info").innerHTML = "When adding "+localeArr.length;
        marker.setDraggable(true);
        google.maps.event.addListener(marker, 'dragend', function() {
            selectedMarker = marker;
            selecterMarkerType = "locale";
            updateLocaleInfoDisplay(marker);
            marker.setIcon('/images/hunting.png');
        });
        google.maps.event.addListener(marker, 'click', function() {
            selectedMarker = marker;
            selecterMarkerType = "locale";
            //   createLocaleInfoDisplay(marker);
            updateLocaleInfoDisplay(marker);
            marker.setIcon('/images/hunting.png');
        });
        createLocaleInfoDisplay(marker);
        updateLocaleInfoDisplay(marker);

        //****************************************************
    }else if(addState=="poi"){
        var markerp = new google.maps.Marker({
            position: location,
            map: map,
            shadow: pShadow,
            icon: aniImage2,
            shape: pShape

        });
        //add the marker to array
        poiArr.push(markerp);
        document.getElementById("info").innerHTML = "When adding "+poiArr.length;
        markerp.setDraggable(true);
        google.maps.event.addListener(markerp, 'dragend', function() {
            selectedMarker = markerp;
            selecterMarkerType = "poi";
            updatePoiInfoDisplay(markerp);
            markerp.setIcon('/images/info.png');
        });
        google.maps.event.addListener(markerp, 'click', function() {
            selectedMarker = markerp;
            selecterMarkerType = "poi";
            //createPoiInfoDisplay();
            updatePoiInfoDisplay(markerp);
            markerp.setIcon('/images/info.png');
        });
        createPoiInfoDisplay(markerp);
        updatePoiInfoDisplay(markerp);

    }
   
}

function findLocationLocale(latlng, ind){
    if (geocoder) {
        geocoder.geocode({
            'latLng': latlng
        }, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                if (results[1]) {
                    document.getElementById("ld" + ind).innerHTML = results[0].formatted_address.toString();
                    localeGeoArr.push(results[0].formatted_address.toString());
                } else {
                    document.getElementById("ld" + ind).innerHTML = "No results found";
                    localeGeoArr.push("No results found");
                }
            } else {
                document.getElementById("ld" + ind).innerHTML = "Geocoder failed due to: " + status;
                localeGeoArr.push("Geocoder failed due to: " + status);
            }
        });
    }
}

function findLocationPoi(latlng, ind){
    if (geocoder) {
        geocoder.geocode({
            'latLng': latlng
        }, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                if (results[1]) {
                    document.getElementById("pd" + ind).innerHTML = results[0].formatted_address.toString();
                    poiGeoArr.push(results[0].formatted_address.toString());
                } else {
                    document.getElementById("pd" + ind).innerHTML = "No results found";
                    poiGeoArr.push("No results found");
                }
            } else {
                document.getElementById("pd" + ind).innerHTML = "Geocoder failed due to: " + status;
                poiGeoArr.push("Geocoder failed due to: " + status);
            }
        });
    }
}

function setMessage(message, type){
    //document.getElementById("message").innerHTML = message;
    if(type == "info"){
        $('#message').text(message);
        $('#message').glow('red', 1000, 200);
    }else if(type == "ins"){
        $('#message').text(message);
        $('#message').glow('blue', 1000, 200);
    }else if(type == "error"){
        $('#message').text(message);
        $('#message').glow('red', 500, 200);
    }
   
}


function createLocaleInfoDisplay(marker){
    var ind = getIndexByMarker(localeArr, marker);
    var eld = document.createElement('div');
    eld.setAttribute("id", "ld" + ind);
    eld.setAttribute("class", "addresstext");
    eld.innerHTML = "Loading...";
    Dom.add(eld, 'localebox');
    var elb = document.createElement('input');
    elb.setAttribute("type", "button");
    elb.setAttribute("id", "lb" + ind);
    elb.setAttribute("class", "removeBtn");
    Dom.add(elb, 'localebox');
}


function createPoiInfoDisplay(marker){
    var ind = getIndexByMarker(poiArr, marker);
    var eld = document.createElement('div');
    eld.setAttribute("id", "pd" + ind);
    eld.setAttribute("class", "addresstext");
    eld.innerHTML = "Loading...";
    Dom.add(eld, 'poibox');
    var elb = document.createElement('input');
    elb.setAttribute("type", "button");
    elb.setAttribute("id", "pb" + ind);
    elb.setAttribute("class", "removeBtn");
    Dom.add(elb, 'poibox');
}

function updateLocaleInfoDisplay(marker){
    //  document.getElementById("ld").innerHTML = "" +
    var ind = getIndexByMarker(localeArr, marker);
    findLocationLocale(marker.getPosition(), ind);
    document.getElementById("lb" + ind).setAttribute("onclick", "removeLocaleMarker("+ind+")");
}

function updatePoiInfoDisplay(marker){
    //  document.getElementById("ld").innerHTML = "" +
    var ind = getIndexByMarker(poiArr, marker);
    findLocationPoi(marker.getPosition(), ind);
    document.getElementById("pb" + ind).setAttribute("onclick", "removePoiMarker("+ind+")");
}

function removeLocaleMarker(index){
    localeArr[index].setMap(null);
    for(var i=0; i<2; i++){
        if(document.getElementById("ld" + i)!=null){
            Dom.remove(document.getElementById("ld" + i));
        }
        if(document.getElementById("lb" + i)!=null){
            Dom.remove(document.getElementById("lb" + i));
        }
    }
    localeArr.splice(index, 1);
    localeGeoArr.splice(index, 1);
    for(var j=0;j<localeArr.length; j++){
        //        var ind = getIndexByMarker(localeArr, marker);
        var eld = document.createElement('div');
        eld.setAttribute("id", "ld" + j);
	 eld.setAttribute("class", "addresstext");
        eld.innerHTML = localeGeoArr[j];
        Dom.add(eld, 'localebox');
        var elb = document.createElement('input');
        elb.setAttribute("type", "button");
        elb.setAttribute("id", "lb" + j);
        elb.setAttribute("class", "removeBtn");
        elb.setAttribute("onclick", "removeLocaleMarker("+j+")");
        Dom.add(elb, 'localebox');
    }
    document.getElementById("info").innerHTML = "When romoving "+localeArr.length;
    setMessage("Location Removed", "info");    
}

function removePoiMarker(index){
    poiArr[index].setMap(null);
    for(var i=0; i<10; i++){
        if(document.getElementById("pd" + i)!=null){
            Dom.remove(document.getElementById("pd" + i));
        }
        if(document.getElementById("pb" + i)!=null){
            Dom.remove(document.getElementById("pb" + i));
        }
    }
    poiArr.splice(index, 1);
    poiGeoArr.splice(index, 1);
    for(var j=0;j<poiArr.length; j++){
        //        var ind = getIndexByMarker(localeArr, marker);
        var eld = document.createElement('div');
        eld.setAttribute("id", "pd" + j);
 	 eld.setAttribute("class", "addresstext");
        eld.innerHTML = poiGeoArr[j];
        Dom.add(eld, 'poibox');
        var elb = document.createElement('input');
        elb.setAttribute("type", "button");
        elb.setAttribute("id", "pb" + j);
        elb.setAttribute("class", "removeBtn");
        elb.setAttribute("onclick", "removePoiMarker("+j+")");
        Dom.add(elb, 'poibox');
    }

    document.getElementById("info").innerHTML = "When romoving "+poiArr.length;
    setMessage("Location Removed", "info");
}

function getIndexByMarker(array, marker){
    for (var i=0; i<array.length; i++) {
        var aposition = array[i].getPosition();
        var mposition = marker.getPosition();
        if((aposition.lat()==mposition.lat())&&(aposition.lng()==mposition.lng())){
            return i;
        }
    }
    return -1;
}


var aniImage = new google.maps.MarkerImage('/images/anicon.gif',
new google.maps.Size(45, 45),
new google.maps.Point(0,0),
new google.maps.Point(0, 45));
    
var aniImage2 = new google.maps.MarkerImage('/images/anicon.gif',
new google.maps.Size(45, 45),
new google.maps.Point(0,0),
new google.maps.Point(0, 45));


var lImage = new google.maps.MarkerImage('/images/hunting.png',
new google.maps.Size(21, 31),
new google.maps.Point(0,0),
new google.maps.Point(0, 31));
var lShadow = new google.maps.MarkerImage('/images/shadow.png',
new google.maps.Size(52, 29),
new google.maps.Point(0,0),
new google.maps.Point(0, 29));
var lShape = {
    coord: [1, 1, 1, 20, 18, 20, 18 , 1],
    type: 'poly'
};

var pImage = new google.maps.MarkerImage('/images/info.png',
new google.maps.Size(21, 31),
new google.maps.Point(0,0),
new google.maps.Point(0, 31));
var pShadow = new google.maps.MarkerImage('/images/shadow.png',
new google.maps.Size(52, 29),
new google.maps.Point(0,0),
new google.maps.Point(0, 29));
var pShape = {
    coord: [1, 1, 1, 20, 18, 20, 18 , 1],
    type: 'poly'
};


var Dom = {
    get: function(el) {
        if (typeof el === 'string') {
            return document.getElementById(el);
        } else {
            return el;
        }
    },
    add: function(el, dest) {
        var el = this.get(el);
        var dest = this.get(dest);
        dest.appendChild(el);
    },
    remove: function(el) {
        var el = this.get(el);
        el.parentNode.removeChild(el);
    }
};
var Event = {
    add: function() {
        if (window.addEventListener) {
            return function(el, type, fn) {
                Dom.get(el).addEventListener(type, fn, false);
            };
        } else if (window.attachEvent) {
            return function(el, type, fn) {
                var f = function() {
                    fn.call(Dom.get(el), window.event);
                };
                Dom.get(el).attachEvent('on' + type, f);
            };
        }
    }()
};

function saveAndContinue(){

    var sendArray = [];
    sendArray.push(document.getElementById("userid").innerHTML);
    for (var i = 0; i < localeArr.length; i++){
        var a = [localeArr[i].getPosition().lat() , localeArr[i].getPosition().lng() , "lacale"];
        sendArray.push(a);
    }

    for (var j = 0; j < poiArr.length; j++){
        var b = [poiArr[j].getPosition().lat() , poiArr[j].getPosition().lng() , "poi"];
        sendArray.push(b);
    }
   
    var sendData = JSON.stringify(sendArray);
    document.getElementById("test").innerHTML = sendData;
    $.post('/localeset/', {
        data: sendData
    }, redirectPage(), "json");
}
function redirectPage(){

    window.location="/thanks/";

}
