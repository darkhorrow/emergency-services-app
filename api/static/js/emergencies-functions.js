$(document).ready(function() {

    emergencies = []

    $("#snt-b").click(function() {
        $("#service-name").attr("value","Sanitary");
    });

    $("#frm-b").click(function() {
        $("#service-name").attr("value","Firemen");
    });

    $("#plc-b").click(function() {
        $("#service-name").attr("value","Policemen");
    });

    $("#ntd-b").click(function() {
        $("#emergency-type").attr("value","natural_disaster");
    });

    $("#tft-b").click(function() {
        $("#emergency-type").attr("value","thief");
    });

    $("#hmc-b").click(function() {
        $("#emergency-type").attr("value","homicide");
    });

    $("#pnd-b").click(function() {
        $("#emergency-type").attr("value","pandemic");
    });

    $("#tfc-b").click(function() {
        $("#emergency-type").attr("value","car_crash");
    });

    $("#service-form").submit(function(e) {
        e.preventDefault();
        var form = $(this);
        var url = "addService";
        $.ajax({
               type: "POST",
               url: url,
               dataType: 'json',
               data: form.serialize(),
               success: function(response) {
                    switch(response.callback.name) {
                      case "Sanitary":
                        addMarker(response.callback.id, "Sanitary", "green", "service");
                        break;
                      case "Firemen":
                        addMarker(response.callback.id, "Firemen", "red", "service");
                        break;
                      case "Policemen":
                        addMarker(response.callback.id, "Policemen", "blue", "service");
                      default:
                        break;
                    }
                    $("#service-modal").modal("hide");
                    $("#log-textarea").append("<p class='text-success'>" + response.callback.name +
                    " service added succesfully</p>");
                    logger(response.logs);
               }
        }).responseJSON;
    });

    $("#emergency-form").submit(function(e) {
        e.preventDefault();
        var form = $(this);
        var url = "addEmergency";
        $.ajax({
               type: "POST",
               url: url,
               data: form.serialize(),
               dataType: 'json',
               success: function(response) {
                    switch(response.callback.type) {
                      case "natural_disaster":
                        addMarker(response.callback.id, "Natural disaster", "orange", "emergency");
                        break;
                      case "thief":
                        addMarker(response.callback.id, "Theft", "orange", "emergency");
                        break;
                      case "homicide":
                        addMarker(response.callback.id, "Homicide", "orange", "emergency");
                        break;
                      case "pandemic":
                        addMarker(response.callback.id, "Pandemic", "orange", "emergency");
                        break;
                      case "car_crash":
                        addMarker(response.callback.id, "Traffic accident", "orange", "emergency");
                        break;
                      default:
                        break;
                    }
                    $("#emergency-modal").modal("hide")
                    $("#log-textarea").append("<p class='text-success'>" + response.callback.type +
                    " emergency added succesfully</p>");
                    logger(response.logs);
               }
        }).responseJSON;
    });

    function addMarker(id, title, color, type) {

        var infoText = "<ul class='list-group'>" +
                            "<li class='list-group-item'><b>ID</b>: " + id +"</li>" +
                            "<li class='list-group-item'><b>Title</b>: " + title +"</li>" +
                            "<li class='list-group-item'><b>Type</b>: " + type +"</li>" +
                        "</ul>";

        var marker = new google.maps.Marker({
            id: id,
            type: type,
            animation: google.maps.Animation.DROP,
            position: new google.maps.LatLng(-15.42843, 28.12504),
            title: title,
            draggable: true,
            map: map,
            icon: {
                url: "http://maps.google.com/mapfiles/ms/icons/" + color + "-dot.png"
            },
            info: new google.maps.InfoWindow({ content: infoText })
        });

        marker.addListener('click', function() {
            marker.info.open(map, marker);
        });


        google.maps.event.addListener(marker, 'dragend', function() {
            if(marker.type == 'service') {
                moveMarker(marker, "moveService");
            } else if(marker.type == 'emergency') {
                moveMarker(marker, "moveEmergency");
            }
        });

        if(type == 'emergency') {
            emergencies.push(marker);
        }
    }

    function moveMarker(marker, url) {
        var id = marker.id;
        var locX = marker.position.lat();
        var locY = marker.position.lng();
        $.ajax({
               type: "POST",
               url: url,
               dataType: 'json',
               data: 'id=' + encodeURIComponent(id) + '&locx=' + encodeURIComponent(locX) + '&locy=' + encodeURIComponent(locY),
               success: function(data) {
                    var type = url == "moveService" ? 'Service' : 'Emergency'
                    $("#log-textarea").append("<p class='text-success'>" + type + "[ID " + id + "] re-allocated succesfully</p>");
               }
        }).responseJSON;
    }

    function removeEmergencyMarker(id) {
        emergencies.forEach(function(marker) {
            if(marker.id == id) {
                console.log("Confirming " + id  + " delete");
                marker.setMap(null);
                var index = emergencies.indexOf(marker);
                if(index > -1) {
                    emergencies.splice(index, 1);
                    console.log("Out of array");
                }
            }
        });
    }

    function logger(logs) {
        var existsError = false;
        var id = -1;
        logs.forEach(function(log) {
            id = log.id_emergency;
            var isError = log.code == -1 ? true : false;
            var color = "text-" + (isError ? "danger" : "success");
            var text = "";
            if(isError) {
                text = "There are not enough " + log.service.toLowerCase() +  "[ID " + log.id_service + "] employees to satisfy the " +
                log.emergency.toLowerCase() + "[ID " + log.id_emergency + "] emergency"
                existsError = true;
            } else {
                text = "The " + log.emergency.toLowerCase() +  "[ID " + log.id_service + "] emergency has been designated to the " +
                log.service.toLowerCase() + "[ID " + log.id_emergency + "]";
            }
            var p = $("#log-textarea").append("<p class='" + color + "'>" + text + "</p>");
        });
        if(!existsError) {
            console.log("Deleting " + id);
            removeEmergencyMarker(id);
        }
    }

});