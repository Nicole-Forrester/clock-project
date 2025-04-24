$( document ).ready(function() {
    $('#clockTable').DataTable( {
        ajax: {
            url: '/data',
            dataSrc: 'clocks'
        }, // Fetch data from Flask
        responsive: true, // Make the table responsive
        columns: [
            { data: 'clock' },
            { data: 'paper' },
            { data: 'num_cpgs' },
            { data: 'species' },
            { data: 'training_tissue',
                render: function (data) {
                    // Check if the data contains commas
                    if (data.includes(',')) {
                        // Split the string by commas to count the tissues
                        const tissues = data.split(',').map(tissue => tissue.trim()); // Remove any leading or trailing spaces from each tissue name after splitting
                        const tooltip = tissues.join(', ');  // Full list of tissues
                        return `
                            <span class="tooltip-container">
                                ${tissues[0]} and ${tissues.length - 1} other tissues
                                <span class="tooltip-text">${tooltip}</span>
                            </span>
                        `;
                    } else {
                        return data; // Show the single tissue name, no tooltip
                    }
                }
            },
            { data: 'training_data_type' },
            { data: 'training_tissue_dup', visible: false },
            { data: 'training_age_range', visible: false },
            { data: 'mad_years', visible: false },
            { data: 'genome_build', visible: false },
            { data: 'method', visible: false },
            { data: 'cpg_locs', visible: false },
            { data: 'language', visible: false },
            { data: 'code', visible: false },
            { data: 'url', visible: false },
            { data: 'kb1to5_cpgs', visible: false },
            { data: 'firstexon_cpgs', visible: false },
            { data: 'utr3_cpgs', visible: false },
            { data: 'utr5_cpgs', visible: false },
            { data: 'body_cpgs', visible: false },
            { data: 'cds_cpgs', visible: false },
            { data: 'exon_cpgs', visible: false },
            { data: 'igr_cpgs', visible: false },
            { data: 'intron_cpgs', visible: false },
            { data: 'promoter_cpgs', visible: false },
            { data: 'gene_cpgs', visible: false },
            { data: 'tss1500_cpgs', visible: false },
            { data: 'tss200_cpgs', visible: false },
            { data: 'no_ucsc_annotation_cpgs', visible: false },
            { data: 'island_cpgs', visible: false },
            { data: 'shore_cpgs', visible: false },
            { data: 'shelf_cpgs', visible: false },
            { data: 'no_island_info_cpgs', visible: false }
        ],
        paging: true,
        order: [],  // Disable initial ordering - don't want clocks to be ordered alphabetically by default
        autoWidth: false, // Prevent automatic resizing
        columnDefs: [
            { width: "16%", "targets": 0 },  // Clock name column
            { width: "16%", "targets": 1 },  // Paper column
            { width: "8%", "targets": 2 }, // Num CpGs column
            { width: "16%", "targets": 3 },  // Species column
            { width: "22%", "targets": 4 },  // Tissues column
            { width: "20%", "targets": 5 },  // Data type column

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