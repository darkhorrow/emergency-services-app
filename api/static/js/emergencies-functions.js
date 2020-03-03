$(document).ready(function() {
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
        addMarker("Natural disaster", "orange");
        var type = "natural_disaster";
        var locX = -15.45;
        var locY = 28.12;
        var nPeople = 100;
        var params = "type=" + type + "&locx=" + locX + "&locy=" + locY + "&npeople=" + nPeople;
        addRequest("addEmergency", params);
    });

    $("#tft-b").click(function() {
        addMarker("Theft", "orange");
        var type = "thief";
        var locX = -15.45;
        var locY = 28.12;
        var nPeople = 1;
        var params = "type=" + type + "&locx=" + locX + "&locy=" + locY + "&npeople=" + nPeople;
        addRequest("addEmergency", params);
    });

    $("#hmc-b").click(function() {
        addMarker("Homicide", "orange");
        var type = "homicide";
        var locX = -15.45;
        var locY = 28.12;
        var nPeople = 20;
        var params = "type=" + type + "&locx=" + locX + "&locy=" + locY + "&npeople=" + nPeople;
        addRequest("addEmergency", params);
    });

    $("#pnd-b").click(function() {
        addMarker("Pandemic", "orange");
        var type = "pandemic";
        var locX = -15.45;
        var locY = 28.12;
        var nPeople = 200;
        var params = "type=" + type + "&locx=" + locX + "&locy=" + locY + "&npeople=" + nPeople;
        addRequest("addEmergency", params);
    });

    $("#tfc-b").click(function() {
        addMarker("Traffic accident", "orange");
        var type = "car_crash";
        var locX = -15.45;
        var locY = 28.12;
        var nPeople = 100;
        var params = "type=" + type + "&locx=" + locX + "&locy=" + locY + "&npeople=" + nPeople;
        addRequest("addEmergency", params);
    });

    $("#service-form").submit(function(e) {
        e.preventDefault();
        var form = $(this);
        var url = "addService";
        $.ajax({
               type: "POST",
               url: url,
               data: form.serialize(),
               success: function(data) {
                    switch(data) {
                      case "Sanitary":
                        addMarker("Sanitary", "green");
                        break;
                      case "Firemen":
                        addMarker("Firemen", "red");
                        break;
                      case "Policemen":
                        addMarker("Firemen", "blue");
                      default:
                        break;
                    }
                    $("#service-modal").modal("hide")
               }
        });
    });

    $("#emergency-form").submit(function(e) {
        e.preventDefault();
        var form = $(this);
        var url = "addEmergency";
        $.ajax({
               type: "POST",
               url: url,
               data: form.serialize(),
               success: function(data) {
                    switch(data) {
                      case "natural_disaster":
                        addMarker("Natural disaster", "orange");
                        break;
                      case "thief":
                        addMarker("Theft", "orange");
                        break;
                      case "homicide":
                        addMarker("Homicide", "orange");
                      default:
                        break;
                    }
                    $("#emergency-modal").modal("hide")
               }
        });
    });

    function addMarker(title, color) {
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(-15.42843, 28.12504),
            title: title,
            draggable: true,
            map: map,
            icon: {
                url: "http://maps.google.com/mapfiles/ms/icons/" + color + "-dot.png"
            }
        });
    }

});