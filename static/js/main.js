window.onload=init;
  function init(){
    const map= new ol.Map({
      view: new ol.View({
        center:[0,0],
        zoom:2
      }),
      layers:[
        new ol.layer.Tile({
          source: new ol.source.OSM()
        })
      ],
      target:'map'
    })
    var data = new ol.layer.IMAGE({
      title:'ecosikh',
      source: new ol.source.IMAGEWMS({
          url:'http://localhost:8080/geoserver/wms',
          params:{'LAYERS':'eco:data'},
          ratio:1,
          serverType:'geoserver'
      })
  });
  }