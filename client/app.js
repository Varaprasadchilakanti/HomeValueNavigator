$(document).ready(function() {
    onPageLoad();
    $('#homePriceForm').submit(function(e) {
        e.preventDefault();
        onClickedEstimatePrice();
    });
});

function onClickedEstimatePrice() {
    var sqft = $('#uiSqft').val();
    var bhk = $("input[name='uiBHK']:checked").val();
    var bathrooms = $("input[name='uiBathrooms']:checked").val();
    var location = $('#uiLocations').val();
    var estPrice = $('#uiEstimatedPrice');
    var loadingOverlay = $('#loadingOverlay');

    var url = "http://127.0.0.1:5000/predict_home_price";

    // Show loading overlay
    loadingOverlay.show();

    $.post(url, {
        total_sqft: parseFloat(sqft),
        bhk: bhk,
        bath: bathrooms,
        location: location
    }, function(data, status) {
        estPrice.html("<h2>" + data.estimated_price + " Lakh</h2>");
        // Hide loading overlay
        loadingOverlay.hide();
    }).fail(function() {
        // Hide loading overlay in case of server disconnect
        loadingOverlay.hide();
        alert("Server disconnected. Please try again later.");
    });
}

function onPageLoad() {
    loadBHKOptions();
    loadBathOptions();
    loadLocations();
}

function loadBHKOptions() {
    var bhkOptions = $('#bhkOptions');
    for (var i = 1; i <= 5; i++) {
        bhkOptions.append('<input type="radio" id="radio-bhk-' + i + '" name="uiBHK" value="' + i + '" required><label for="radio-bhk-' + i + '">' + i + '</label>');
    }
}

function loadBathOptions() {
    var bathOptions = $('#bathOptions');
    for (var i = 1; i <= 5; i++) {
        bathOptions.append('<input type="radio" id="radio-bath-' + i + '" name="uiBathrooms" value="' + i + '" required><label for="radio-bath-' + i + '">' + i + '</label>');
    }
}

function loadLocations() {
    var url = "http://127.0.0.1:5000/get_location_names";
    $.get(url, function(data, status) {
        if(data && data.locations) {
            var locations = data.locations;
            var uiLocations = $('#uiLocations');
            uiLocations.empty();
            $.each(locations, function(index, location) {
                uiLocations.append($('<option>', {
                    value: location,
                    text: location
                }));
            });
        }
        else {
            $('#uiLocations').html('<option value="" disabled selected>No locations available</option>');
        }
    });
}
