$( document ).ready(function() {
    $('#clockTable').DataTable( {
        ajax: '/data', // Fetch data from Flask
        columns: [
            { data: 'clock' },
            { data: 'training_data_type' },
            { data: 'species' },
            { data: 'training_species' },
            { data: 'training_age_range' },
            { data: 'mad_years' },
            { data: 'num_cpgs' },
            { data: 'genome_build' },
            { data: 'method' },
            { data: 'cpg_locs' },
            { data: 'language' },
            { data: 'code' },
            { data: 'paper' },
            { data: 'url' }
        ],
        paging: true,
        order: [],  // Disable initial ordering - don't want clocks to be ordered alphabetically by default
        autoWidth: false, // Prevents automatic resizing
        columnDefs: [
            { width: "2px", "targets": 11 },  // Code column
            { width: "5px", "targets": 13 }  // URL column
        ],
    });
});