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
                      case "pandemic":
                        addMarker("Pandemic", "orange");
                        break;
                      case "car_crash":
                        addMarker("Traffic accident", "orange");
                        break;
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