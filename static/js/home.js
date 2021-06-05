function loadMap() {
  var platform = new H.service.Platform({
  'apikey': 'dpyW2Iu573KvzXn2Mv67G46FCiXJxPBmPXsdVbMd4zs'
  });

  var defaultLayers = platform.createDefaultLayers();

  var map = new H.Map(
    document.getElementById('mapContainer'),
    defaultLayers.vector.normal.map,
    {
      zoom: 8,
      center: { lat: RECOMENDED_LOT[0], lng: RECOMENDED_LOT[1]},
    });
  
  // Enable the event system on the map instance:
  var mapEvents = new H.mapevents.MapEvents(map);

  // Add event listeners:
  map.addEventListener('tap', function(evt) {
      // Log 'tap' and 'mouse' events:
      console.log(evt.type, evt.currentPointer.type);
  });
  // TODO add marker printing

  // Instantiate the default behavior, providing the mapEvents object:
  var behavior = new H.mapevents.Behavior(mapEvents);

  map.addLayer(defaultLayers.vector.normal.traffic);

  // Create a group that can hold map objects:
  group = new H.map.Group();

  // Add the group to the map object (created earlier):
  map.addObject(group);

  // Create an icon, an object holding the latitude and longitude, and a marker:
  // some error in here first we can't find the path of the image
  //"./static/red_marker.png"
  //"./static/blue_marker.png"
  //"./static/black_marker.png"
  var recomended_icon = new H.map.Icon("./static/red_marker.png", {size: {w: 64, h: 64}}),
  lot_icon = new H.map.Icon("./static/blue_marker.png", {size: {w: 48, h: 48}}),
  park_icon = new H.map.Icon("./static/black_marker.png", {size: {w: 48, h: 48}}) 
  
  LIST_OF_LOTS.forEach(element => {
    var lat_marker = element[0];
    var long_marker = element[1];
    var loc = {lat: lat_marker, lng: long_marker}
    if (isRecommendedLot(lat_marker, long_marker)){
      group.addObject(new H.map.Marker(loc, {icon: recomended_icon}))
    }
    else{
      group.addObject(new H.map.Marker(loc, {icon: lot_icon}))
    }
  });

  LIST_OF_PARKS.forEach(element => {
    var lat_marker = element[0];
    var long_marker = element[1];
    var loc = {lat: lat_marker, lng: long_marker}
    if (isRecommendedLot(lat_marker, long_marker)){
      group.addObject(new H.map.Marker(loc, {icon: recomended_icon}))
    }
    else{
      group.addObject(new H.map.Marker(loc, {icon: park_icon}))
    }
  });

  const isMapAnimated = true;
  map.setZoom(14, isMapAnimated);
}

function isRecommendedLot(latitude, longitude){
  return (latitude === RECOMENDED_LOT[0]) && (longitude === RECOMENDED_LOT[1])
}

document.addEventListener('DOMContentLoaded', function() {
  console.log('DOM is ready');
  loadMap();
});

