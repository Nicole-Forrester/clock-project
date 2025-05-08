document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const spinner = document.getElementById("clock-spinner");

    // Spinner on form submit
    if (form && spinner) {
        form.addEventListener("submit", function () {
            spinner.style.display = "flex";
            setTimeout(() => {
                if (document.querySelector(".flash-error")) {
                    spinner.style.display = "none";
                }
            }, 500); // give server time to respond
        });
    }

    // Select2 initialisation with "Select All"
    const select = $('#clock_name');
    const allClockValues = [
        "HorvathS2013", "HannumG2013", "HorvathS2018",
        "LevineM2018", "YangZ2016", "epiTOC2", "DunedinPACE"
    ];

    if (select.length) {
        select.select2({
            placeholder: "Select one or more clocks",
            allowClear: true
        });

        select.on('select2:select', function (e) {
            if (e.params.data.id === 'select_all') {
                select.val(allClockValues).trigger('change');
            }
        });
    }
});