
window.pageMapVehicleOnline = function ()
{
    var article = $("article");
    var divMapId = article.find("#mapId");
    var Online = function ()
    {
        var views = [];
        this.addView = function (view)
        {
            view.online = this;
            view.onAdd();
            views.push(view);
        }
        var withView = function (wv) { for (var i = 0; i < views.length; i++) wv.bind(this)(views[i]); }.bind(this);

        var vehicles = {};
        this.receive = function (vehiclePlate, vehicleState)
        {
            var vehicle = vehicles[vehiclePlate];
            if (vehicle == null) vehicle = vehicles[vehiclePlate] = { VehiclePlate: vehiclePlate };

            var oldState = vehicle.state;
            vehicle.state = vehicleState;
            vehicle.oldState = oldState;

            withView(function (v) { v.show(vehicle); });
        }

        var currentVehicleActive = null;
        var activeHelper = function (vehicle)
        {
            currentVehicleActive = vehicle;
            currentVehicleActive.active = true;
            withView(function (v) { v.active(currentVehicleActive); });
        }

        this.active = function (vehicle)
        {
            if (currentVehicleActive == null) activeHelper(vehicle);            
            else
            {
                currentVehicleActive.active = false;
                withView(function (v) { v.deactive(currentVehicleActive); });
                if (currentVehicleActive.state.VehiclePlate != vehicle.state.VehiclePlate) activeHelper(vehicle);
                else
                {   
                    currentVehicleActive = null;
                }
            }
        }
    }

    var View = function ()
    {
        this.online = null;
        this.onAdd = function () { };
        this.show = function (vehicle) { };
        this.active = function (vehicle) { };
        this.deactive = function (vechile) { };
    }

    
    var TableView = function ()
    {
        $.extend(this, new View());
        this.container = null;
        var tableBody = null;

        this.onAdd = function ()
        {            
            this.container.find(".area-online").remove();
            var area = $("<div class='area-online box' style='position:absolute; width: 190px; bottom: 2px; left: 2px; z-index:999; padding: 1px'>");
            area.append(article.find("[data-form=template]").html());
            this.container.append(area);
            tableBody = area.find(".table-ul-body .table-ul");
        }
        this.show = function (vehicle)
        {
            if (vehicle.row == null)
            {
                var $this = this;
                var row = $("<ul>"); row.css("cursor", "pointer");
                row.append("<li class='col0'>{0}</li>".format(vehicle.VehiclePlate));
                var col2 = $("<li class='col3'></li>"); row.append(col2);
                vehicle.row = row;
                vehicle.col2 = col2;                
                vehicle.row.click(function () { 
                    
                    
                    $this.online.active(vehicle);
                    console.log(data[vehicle['VehiclePlate']])
                
                });
                tableBody.append(row);
            }
            vehicle.col2.html("{0}, {1}".format(vehicle.state.v, vehicle.state.k));
        }
        this.active = function (vehicle) { vehicle.row.addClass("bg-success text-white"); };
        this.deactive = function (vehicle) { vehicle.row.removeClass("bg-success text-white"); };
    }
    var MapView = function ()
    {
        $.extend(this, new View());
        this.map = null;

        var vehicleIcons = [];        
        for (var i = 0; i <= 7; i++)
        {
            vehicleIcons.push("./icon.svg".format(i));            
        }

        this.show = function (vehicle)
        {
            if (vehicle.marker == null)
            {
                var $this = this;
                vehicle.marker = L.marker([vehicle.state.v, vehicle.state.k], { zIndexOffset: 1000 });
                var iconElement = $("<div><div class='badge badge-success' style='font-size:10px'>{0}</div><img class='iconmap' src='' /></div>".format(vehicle.VehiclePlate));
                var markerIcon = L.divIcon({ className: 'vehicle-icon', html: iconElement[0], iconSize: [0, 0], iconAnchor: [0, 0] });
                vehicle.marker.setIcon(markerIcon);
                vehicle.imgIcon = iconElement.find("img");
                vehicle.labelPlate = iconElement.find(".badge");
                vehicle.marker.addTo(this.map);
                vehicle.imgIcon.attr("src", vehicleIcons[Core.random(8)]);
                vehicle.marker.on("click", function () { $this.online.active(vehicle); });
            }
            else
            {
                if (vehicle.oldState == null) vehicle.direction = Core.random(8);
                else vehicle.direction = getDir(vehicle.direction, vehicle.oldState.v, vehicle.oldState.k, vehicle.state.v, vehicle.state.k);

                vehicle.marker.setLatLng(L.latLng(vehicle.state.v, vehicle.state.k));
                vehicle.imgIcon.attr("src", vehicleIcons[vehicle.direction]);

                if (vehicle.active)
                    this.active(vehicle);
            }
        }
        this.active = function (vehicle)
        {
            vehicle.labelPlate.removeClass("badge-success").addClass("badge-danger");
            this.map.panTo(vehicle.marker.getLatLng(), { animate: true });
        }
        this.deactive = function (vehicle)
        {
            vehicle.labelPlate.removeClass("badge-danger").addClass("badge-success");
        }

        var getDir = function (oldDir, oldLatitude, oldLongitude, latitude, longitude)
        {
            //First point
            if (oldLatitude === 0 && oldLongitude === 0) return Core.random(8);

            //If longitude and latitude are not valid, don't change car's direction
            if (longitude === 0 | latitude === 0) { return oldDir; }

            //If distance between two cars is too small, exit sub
            if (canculatorDistance(longitude, latitude, oldLongitude, oldLatitude) < 30) return oldDir;

            //Calculate new direction
            var deltax = 0;
            var deltay = 0;
            var s = 0;
            var g = 0;

            deltax = latitude - oldLatitude;
            deltay = longitude - oldLongitude;

            s = Math.sqrt(Math.pow(deltax, 2) + Math.pow(deltay, 2));
            g = Math.acos(deltax / s);

            if (deltay < 0) { g = 2 * Math.PI - g; }

            g = Math.round(4 * g / Math.PI);
            if (g > 7 || g < 0) { g = 0; }

            return g;
        };
        var canculatorDistance = function (lng1, lat1, lng2, lat2)
        {
            if (lng1 === lng2 && lat1 === lat2) return 0;
            var p1x = lng1 * (Math.PI / 180);
            var p1y = lat1 * (Math.PI / 180);
            var p2x = lng2 * (Math.PI / 180);
            var p2y = lat2 * (Math.PI / 180);

            var kc = p2x - p1x;
            var temp = Math.cos(kc);
            temp = temp * Math.cos(p2y);
            temp = temp * Math.cos(p1y);
            kc = Math.sin(p1y);
            kc = kc * Math.sin(p2y);
            temp = temp + kc;
            kc = Math.acos(temp);
            kc = kc * 6378137;
            return kc;
        };
    }
    
    var map = L.map(divMapId[0]).setView([20.84703, 106.6856], 14);
    //map.options.minZoom = 14;
    //map.options.maxZoom = 14;

    var myUrl = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';
    L.tileLayer(myUrl, { maxZoom: 40, id: 'mapbox/streets-v11', tileSize: 512, zoomOffset: -1 }).addTo(map);

    var online = new Online();

    var tableView = new TableView();
    tableView.container = divMapId;
    online.addView(tableView);

    var mapView = new MapView();
    mapView.map = map;
    online.addView(mapView);

    var ViturlSocket = function (online, data)
    {
        var vehiclePlates = Object.keys(data);
        var onVehicle = function (action)
        {
            for (var i = 0; i < vehiclePlates.length; i++)
            {
                var veiclePlate = vehiclePlates[i];
                action(data[veiclePlate], veiclePlate);
            }
        }.bind(this);
        
        var timer;

        this.start = function ()
        {            
            onVehicle(function (vehicle) { vehicle.currentTrackingIndex = 0; });
            timer = new Core.Timer({ interval: 500 });
            timer.setOption(function (options)
            {
                options.onTick = function ()
                {
                    onVehicle(function (vehicle, vehiclePlate)
                    {
                        var state = vehicle.t[vehicle.currentTrackingIndex];
                        state.VehiclePlate = vehiclePlate;
                        vehicle.currentTrackingIndex++;
                        if (vehicle.currentTrackingIndex >= vehicle.c) vehicle.currentTrackingIndex = 0;

                        online.receive(vehiclePlate, state);
                    });
                }                
            });
            timer.start();
        }
    }
    var viturlSocket = new ViturlSocket(online, data);
    viturlSocket.start();
}