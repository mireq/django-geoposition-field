(function() {

var eventClasses = {
	click: MouseEvent
};
function triggerEvent(element, name, memo, bubbles) {
	var cls = eventClasses[name] || Event;
	var event = new cls(name, {bubbles: bubbles === false ? false : true, cancelable: true});
	event.memo = memo || { };
	element.dispatchEvent(event);
}

function bindEvent(element, name, fn) {
	if (document.addEventListener) {
		element.addEventListener(name, fn, false);
	}
	else {
		element.attachEvent('on' + name, fn);
	}
}

function onLoad(callback) {
	if (document.body) {
		callback({memo: document.body});
		bindEvent(document.body, 'contentloaded', callback);
	}
	else {
		document.addEventListener("DOMContentLoaded", function(event) {
			callback({memo: document.body});
			bindEvent(document.body, 'contentloaded', callback);
		});
	}
}

function createWidgets() {
	var geopositions = window._geopositions || [];
	for (var i = 0, leni = geopositions.length; i < leni; i++) {
		var geoposition = geopositions[i];
		createWidget(geoposition);
	}
	window._geopositions = [];
}

function createWidget(opts) {
	var name = opts.name;
	var container = document.getElementById('id_' + name);
	var widgetContainer = document.getElementById('widget_' + name);

	var latInput = document.getElementById('id_' + name + '_0');
	var lngInput = document.getElementById('id_' + name + '_1');

	createMap({
		container: container,
		latInput: latInput,
		lngInput: lngInput
	});

	widgetContainer.style.display = 'none';
}

function createMap(opts) {
	var mapElement = document.createElement('DIV');
	mapElement.style.width = '100%';
	mapElement.style.height = '100%';
	opts.container.appendChild(mapElement);

	var raster = new ol.layer.Tile({
		//source: new ol.source.MapQuest({layer: 'sat'})
		source: new ol.source.OSM()
	});


	var ClearControl = function(opt_options) {
		var options = opt_options || {};

		var button = document.createElement('button');
		button.innerHTML = 'x';

		var this_ = this;
		var handleClear = function(event) {
			features.clear();
			opts.lngInput.value = '';
			opts.latInput.value = '';
			event.preventDefault();
			event.stopPropagation();
		};

		button.addEventListener('click', handleClear, false);
		button.addEventListener('touchstart', handleClear, false);

		var element = document.createElement('div');
		element.className = 'clear-position ol-unselectable ol-control';
		element.appendChild(button);

		ol.control.Control.call(this, {
			element: element,
			target: options.target
		});
	};
	ol.inherits(ClearControl, ol.control.Control);

	var lng = parseFloat(opts.lngInput.value, 10);
	var lat = parseFloat(opts.latInput.value, 10);

	var viewSettings = {
		center: ol.proj.fromLonLat([19.78, 48.65]),
		zoom: 7
	};
	if (lng && lat) {
		viewSettings = {
			center: ol.proj.fromLonLat([lng, lat]),
			zoom: 13
		};
	}

	var map = new ol.Map({
		layers: [raster],
		target: mapElement,
		view: new ol.View(viewSettings),
		controls: ol.control.defaults({
			attributionOptions: ({
				collapsible: false
			})
		}).extend([
			new ClearControl()
		])
	});

	var features = new ol.Collection();
	var featureOverlay = new ol.layer.Vector({
		source: new ol.source.Vector({features: features}),
		style: new ol.style.Style({
			fill: new ol.style.Fill({
				color: 'rgba(255, 255, 255, 0.2)'
			}),
			stroke: new ol.style.Stroke({
				color: '#0088ff',
				width: 2
			}),
			image: new ol.style.Circle({
				radius: 7,
				fill: new ol.style.Fill({
					color: '#0088ff'
				})
			})
		})
	});
	featureOverlay.setMap(map);

	function setMapCoordinates(lng, lat) {
		var coord = ol.proj.transform([lng, lat], 'EPSG:4326', 'EPSG:3857');
		var feature = new ol.Feature({
			geometry: new ol.geom.Point(coord)
		});
		features.clear();
		features.extend([feature]);
	}

	map.on('click', function(e) {
		var coord = ol.proj.transform(e.coordinate, 'EPSG:3857', 'EPSG:4326');
		opts.lngInput.value = coord[0];
		opts.latInput.value = coord[1];
		triggerEvent(opts.lngInput, 'change');
		triggerEvent(opts.latInput, 'change');
	});

	if (!isNaN(lng) && !isNaN(lat)) {
		setMapCoordinates(lng, lat);
	}

	function onPositionChanged() {
		var lng = parseFloat(opts.lngInput.value, 10);
		var lat = parseFloat(opts.latInput.value, 10);
		if (!isNaN(lng) && !isNaN(lat)) {
			setMapCoordinates(lng, lat);
		}
	}

	bindEvent(opts.lngInput, 'change', onPositionChanged);
	bindEvent(opts.latInput, 'change', onPositionChanged);
}

onLoad(createWidgets);

}());
