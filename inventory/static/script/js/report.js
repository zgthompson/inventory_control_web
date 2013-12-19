report = {
    /* attach tablesorter functionality to report table
     */
    attach_tablesorter: function() {
        $('#report-table').tablesorter();
    },

    /* Converts the relevant values to a function string
     */
    create_function_string: function (type, begin, end) {
        var function_string = "Dajaxice.inventory.";
        function_string += type.toLowerCase().replace(" ", "_");
        function_string += "( Dajax.process, { begin:'" + begin + "',end:'" + end +"'});";
        return function_string;
    },
    /* generate a report based on the current inputs
     */
    generate: function() {
        var type = $('#report-type').val();
        var begin = $('#start-date').val();
        var end = $('#end-date').val();
        eval( report.create_function_string(type, begin, end) );
    },
    /* assign calendar view to datepicker div and attach click listener
     * to the generate button
     */
    init: function() {
        $('#datepicker').datepicker( { autoclose: true } );
        $('#generate').click( report.generate );
    }
};

$( report.init );
