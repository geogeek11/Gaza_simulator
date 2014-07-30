function getColor(d) {
//var ar=['#FFFFB2','#FECC5C','#FD8D3C' ,'#E31A1C' ];
var ar=['#EF0000','#A0CFEC','#FFFFFF' ,'#88419D' ];
if (d== 'Gaza') 
    return ar[0];
else if (d== 'Israel') 
    return ar[1];
else 
	return ar[2];
}

function getalpha(d) {
//var ar=['#FFFFB2','#FECC5C','#FD8D3C' ,'#E31A1C' ];
var ar=[0.8,0.5,0 ,'#88419D' ];
if (d== 'Gaza') 
    return ar[0];
else if (d== 'Israel') 
    return ar[1];
else 
	return ar[2];
}
function highlightFeature(e) {
var layer = e.target;
var lbl ; 
   if(layer.feature.name == "Israel" ||  layer.feature.name  =="Gaza")
lbl =' <h1>' +layer.feature.name+' </h1><br> has hosted <span class = "rfg">'+pop_label(layer.feature.pop)+'</span> palestinian resident and refugee.' ; //+pop_label(feature.pop)
else
lbl =' <h1>'+layer.feature.name+'</h1><br> has  hosted  <span class = "rfg">'+pop_label(layer.feature.pop)+'</span> palestinian refugee.' ; //+pop_label(feature.pop)
    info.update(lbl);
}



function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
}
function resetHighlight(e) {
 
    info.update('Hover over a country recieving refugees');
}
function pop_label(n){

if(n < 1000)
return Math.round(n) ; 
else if(n < 1000000)
return Math.round(n/1000) + "miles" ; 
else
return Math.round(n/1000000 * 100) / 100 + " millions" ; 
}

function style(feature) {
    return {
        fillColor:  getColor(feature.name),
        weight: 1,
        opacity: 1,
        color: 'white',
        //dashArray: '1',
        fillOpacity:getalpha(feature.name)
    };
}


var initial_center = [28.536132122854514,-4.394531259];
var initial_zoom = 2;
var cmAttr = 'Map data &copy; 2011 OpenStreetMap contributors, Imagery &copy; 2011 CloudMade', cmUrl = 'http://{s}.tile.cloudmade.com/2796cd5ac9ce4ede8860581bcef53fba/{styleId}/256/{z}/{x}/{y}.png';
mapLayersList = [ L.tileLayer(cmUrl, {styleId: 67367, attribution: cmAttr})]  //96931
var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var osmAttrib='Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
var street_layer = new L.TileLayer(osmUrl, {minZoom: 8, maxZoom: 18, attribution: osmAttrib});
map = new L.Map('map',{
                center: initial_center,
                zoom: initial_zoom,
                layers: mapLayersList     
				//maxBounds : [[ 37.7039 , -17.1839], [ 20.7460 , -1.0658]]
});
map.on('dblclick', reverse_geocoding) ; 
//center of palestine
var state_center_x; 
var state_center_y; 
        var npoints = 1000;
        var offset = 0;
        var coords = [];
        var points = [];
        var snap_tolerance = 500000;
 
 function load_json(country)
 {
 //console.log(country) ; 
 
 map.eachLayer(function (layer) {
  
 if(  typeof   layer.options === 'undefined'  )
  map.removeLayer(  layer);
  else if(typeof   layer.options.opacity === 'undefined' || layer.options.opacity !=1)
  map.removeLayer(  layer);
});

var host="" ; 

if(location.host !='')
	host  = location.host+"/"
 host="http://raw.githubusercontent.com/geogeek11/geogeek11.github.io/master/" ; 
$.getJSON( host+ "geojson/"+country+".json", function(data) {
	console.log(host+"geojson/"+country+".json") ; 
	features=[] ; 
	//When GeoJSON is loaded
	var geojsonLayer = new L.GeoJSON(data , {style: style , onEachFeature: function (feature, layer) {
         
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight ,
		dblclick : reverse_geocoding ,
		click : zoomToFeature
    });



		if(typeof state_center_x === 'undefined' ||  state_center_x == null) {
		console.log(feature.name)
		state_center_x =  feature.x;
		state_center_y =  feature.y;
		//killed = feature.causalities ; 
		setTimeout(function(){
    odometer1.innerHTML = feature.causalities;
							}, 0);
		setTimeout(function(){
    odometer2.innerHTML = feature.refugies;
							}, 0);	

	country2.innerHTML=feature.real_name ; 
		//legend.update(feature.causalities)
		}
		else
		{
		
		var pointA = new L.LatLng(state_center_y, state_center_x);
var pointB = new L.LatLng(feature.y, feature.x);
var pointList = [pointA, pointB];

var firstpolyline = new L.Polyline(pointList, {
color: 'red',
weight: 2,
opacity: 0.3,
smoothFactor: 0.5 

});
firstpolyline.addTo(map);
		
		

}

var lbl ; 
lbl =feature.name ; 
     }
	 });		//New GeoJSON layer
	 geojsonLayer.addTo(map);
	//map.addLayer(geojsonLayer);			//Add layer to map	
state_center_x = null ; 
});
}

var info = L.control({position: 'topright'});
 
 
info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info legend2'); // create a div with a class "info"
    this.update();
    return this._div;
};

// method that we will use to update the control based on feature properties passed
info.update = function (props) {
    this._div.innerHTML = props;
};

info.addTo(map);

info.update("Double click on a country to simulate");

function reverse_geocoding(e){

$.ajax({
    type: "GET",
    url: "http://nominatim.openstreetmap.org/reverse?format=json&lat="+e.latlng.lat+"&lon="+e.latlng.lng,
    dataType: 'json',
    success: function (response) {
load_json(response.address.country_code) ; 

    }
});


}
