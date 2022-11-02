function isRecommendedLot(latitude, longitude){
  return (latitude === RECOMENDED_LOT[0]) && (longitude === RECOMENDED_LOT[1])
}

/**
 * Creates a new marker and adds it to a group
 * @param {H.map.Group} group       The group holding the new marker
 * @param {H.geo.Point} coordinate  The location of the marker
 * @param {String} html             Data associated with the marker
 */
 function addMarkerToGroup(group, marker_icon, coordinate, html) {
  var marker = new H.map.Marker(coordinate, {icon: marker_icon});
  // add custom data to the marker
  marker.setData(html);
  group.addObject(marker);
}

function addInfoBubble(map, ui) {
  var group = new H.map.Group();

  map.addObject(group);

  // add 'tap' event listener, that opens info bubble, to the group
  /*group.addEventListener('tap', function (evt) {
    // event target is the marker itself, group is a parent event target
    // for all objects that it contains
    var bubble = new H.ui.InfoBubble(evt.target.getGeometry(), {
      // read custom data
      content: evt.target.getData()
    });
    // show info bubble
    ui.addBubble(bubble);
  }, false);*/

  // Create an icon, an object holding the latitude and longitude, and a marker:
  // some error in here first we can't find the path of the image
  //"./static/red_marker.png"
  //"./static/blue_marker.png"
  //"./static/black_marker.png"
  var recomended_icon = new H.map.Icon("./static/red_marker.png", {size: {w: 64, h: 64}}),
  lot_icon = new H.map.Icon("./static/blue_marker.png", {size: {w: 48, h: 48}}),
  park_icon = new H.map.Icon("./static/black_marker.png", {size: {w: 48, h: 48}}) 
  
  LIST_OF_LOTS.forEach(element => {
    var name = element[0];
    var address = element[1];
    var lat_marker = element[2];
    var long_marker = element[3];
    var loc = {lat: lat_marker, lng: long_marker};
    var info_html = `<div><p><b>${name}</p></b></div>` + `<div><p><b>Adres:</b> ${address}</p></div>` + `<div><a href="https://www.google.com/maps/search/?api=1&query=${lat_marker},${long_marker}" target="_blank">Google Maps'e yönlendir</a></div>`;
    if (isRecommendedLot(lat_marker, long_marker)){
      addMarkerToGroup(group, recomended_icon, loc, info_html);
    }
    else{
      addMarkerToGroup(group, lot_icon, loc, info_html);
    }
  });

  LIST_OF_PARKS.forEach(element => {
    var name = element[0];
    var address = element[1];
    var lat_marker = element[2];
    var long_marker = element[3];
    var loc = {lat: lat_marker, lng: long_marker};
    var info_html = `<div><p><b>${name}</p></b></div>` + `<div><p><b>Adres:</b> ${address}</p></div>` + `<div><a href="https://www.google.com/maps/search/?api=1&query=${lat_marker},${long_marker}" target="_blank">Google Maps'e yönlendir</a></div>`;
    if (isRecommendedLot(lat_marker, long_marker)){
      addMarkerToGroup(group, recomended_icon, loc, info_html);
    }
    else{
      addMarkerToGroup(group, park_icon, loc, info_html);
    }
  });
}

function loadMap() {
  var platform = new H.service.Platform({
  'apikey': 'H9eImXWLstldKWISj-5HXAkiQpP5IOyV_uXjAc6lkyw'
  });

  var defaultLayers = platform.createDefaultLayers();

  var map = new H.Map(
    document.getElementById('mapContainer'),
    defaultLayers.vector.normal.map,
    {
      zoom: 8,
      center: { lat: RECOMENDED_LOT[0], lng: RECOMENDED_LOT[1]},
    });

  map.addEventListener('tap', evt => {
    ui.getBubbles().forEach(bub => ui.removeBubble(bub));

    if(!evt.target.getData) return;
    // for all objects that it contains
    var bubble =  new H.ui.InfoBubble(evt.target.getGeometry(), {
        // read custom data
        content: evt.target.getData()
    });
    // show info bubble
    ui.addBubble(bubble);
    bubble.addClass("H_ib_noclose")
  });
  
  // Enable the event system on the map instance:
  //var mapEvents = new H.mapevents.MapEvents(map);

  // Instantiate the default behavior, providing the mapEvents object:
  //var behavior = new H.mapevents.Behavior(mapEvents);

  map.addLayer(defaultLayers.vector.normal.traffic);

  // create default UI with layers provided by the platform
  //var ui = H.ui.UI.createDefault(map, defaultLayers);

  //addInfoBubble(map, ui)

  const isMapAnimated = true;
  map.setZoom(14, isMapAnimated);

  window.addEventListener('resize', () => map.getViewPort().resize());
}

document.addEventListener('DOMContentLoaded', function() {
  console.log('DOM is ready');
  loadMap();
});

