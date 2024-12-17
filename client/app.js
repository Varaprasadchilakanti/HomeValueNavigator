$(document).ready(function () {
    const API_BASE_URL = "http://127.0.0.1:5000"; // API Base URL

    onPageLoad();

    $('#homePriceForm').submit(function (e) {
        e.preventDefault();
        onClickedEstimatePrice();
    });

    function onClickedEstimatePrice() {
        const sqft = parseFloat($('#uiSqft').val());
        const bhk = $("input[name='uiBHK']:checked").val();
        const bathrooms = $("input[name='uiBathrooms']:checked").val();
        const location = $('#uiLocations').val();
        const estPrice = $('#uiEstimatedPrice');
        const loadingOverlay = $('#loadingOverlay');

        if (!sqft || !bhk || !bathrooms || !location) {
            estPrice.html('<h2 style="color: var(--error-color)">Please fill all fields correctly.</h2>');
            return;
        }

        loadingOverlay.show();

        $.post(`${API_BASE_URL}/predict_home_price`, {
            total_sqft: sqft,
            bhk: bhk,
            bath: bathrooms,
            location: location
        })
            .done(function (data) {
                estPrice.html(`<h2>${data.estimated_price} Lakh</h2>`);
            })
            .fail(function () {
                estPrice.html('<h2 style="color: var(--error-color)">Server Error. Try again later.</h2>');
            })
            .always(function () {
                loadingOverlay.hide();
            });
    }

    function onPageLoad() {
        appendOptions('bhkOptions', 5, 'BHK');
        appendOptions('bathOptions', 5, 'Bathrooms');
        loadLocations();
    }

    function appendOptions(containerId, count, groupName) {
        const container = $(`#${containerId}`);
        container.empty();
        for (let i = 1; i <= count; i++) {
            container.append(`
                <input type="radio" id="radio-${groupName}-${i}" name="ui${groupName}" value="${i}" required>
                <label for="radio-${groupName}-${i}">${i}</label>
            `);
        }
    }

    function loadLocations() {
        const url = `${API_BASE_URL}/get_location_names`;
        $.get(url)
            .done(function (data) {
                if (data && data.locations) {
                    const uiLocations = $('#uiLocations');
                    uiLocations.empty();
                    data.locations.forEach(location => {
                        uiLocations.append(`<option value="${location}">${location}</option>`);
                    });
                }
            })
            .fail(function () {
                $('#uiLocations').html('<option value="" disabled selected>No locations available</option>');
            });
    }
});
