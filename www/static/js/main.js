$( document ).ready(function() {
    $('#clockTable').DataTable( {
        ajax: '/data', // Fetch data from Flask
        responsive: true, // Make the table responsive
        columns: [
            { data: 'clock' },
            { data: 'training_data_type' },
            { data: 'species' },
            { data: 'training_tissue',
                render: function (data) {
                    // Check if the data contains commas
                    if (data.includes(',')) {
                        // Split the string by commas to count the tissues
                        const tissues = data.split(',').map(tissue => tissue.trim()); // Remove any leading or trailing spaces from each tissue name after splitting
                        return `${tissues[0]} and ${tissues.length - 1} other tissues` // Show count of tissues
                    } else {
                        return data; // Show the single tissue name
                    }
                }
            },
            { data: 'paper' },
            { data: 'training_tissue_dup', visible: false },
            { data: 'training_age_range', visible: false },
            { data: 'mad_years', visible: false },
            { data: 'num_cpgs', visible: false },
            { data: 'genome_build', visible: false },
            { data: 'method', visible: false },
            { data: 'cpg_locs', visible: false },
            { data: 'language', visible: false },
            { data: 'code', visible: false },
            { data: 'url', visible: false }
        ],
        paging: true,
        order: [],  // Disable initial ordering - don't want clocks to be ordered alphabetically by default
        autoWidth: false, // Prevent automatic resizing
        columnDefs: [
            { width: "15%", "targets": 0 },  // Clock name column
            { width: "25%", "targets": 1 },  // Data type column
            { width: "15%", "targets": 2 },  // Species column
            { width: "25%", "targets": 3 },  // Tissues column
            { width: "20%", "targets": 4 },  // Paper column
        ],
        rowCallback: function (row, data) {
            // Add click event to each row
            $(row).css('cursor', 'pointer');  // Change cursor to pointer to indicate clickable row
            $(row).on('click', function () {
                window.location.href = `/clock/${encodeURIComponent(data.clock)}`;
            });
        }
    });
});