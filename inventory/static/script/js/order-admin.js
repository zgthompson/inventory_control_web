var orderFormAdmin = {
    
    /* Sets job in internal representation and updates the input to display
     * the job number
     */
    select_job: function(e) {
        var cur_job = $(e).attr('data');
        // parent of parent is the row
        var cur_row = e.parentElement.parentElement;
        // first child contains the job number
        var number = cur_row.children[0].innerHTML;
        // internal representation
        orderForm.order.job = cur_job;
        // update input field
        $('#job-name').val(number);
        // erase table
        $('#job-results').html("");
        // clear search form
        $('#job-search').val("");
    },

    /* Sets employee in internal representation and updates the input to display
     * the employee name 
     */
    select_employee: function(e) {
        var cur_employee = $(e).attr('data');
        // parent of parent is the row
        var cur_row = e.parentElement.parentElement;
        // first child contains the job number
        var name = cur_row.children[0].innerHTML;
        // internal representation
        orderForm.order.employee = cur_employee;
        // update input field
        $('#employee-name').val(name);
        // erase table
        $('#employee-results').html("");
        // clear search form
        $('#employee-search').val("");
    },

    /* Set employee name and job name fields to readonly, they will
     * automatically be set by the employee/job search and attach
     * keyup listeners to the job and employee search fields
     */
    init: function() {
        $('#employee-name').prop('readonly', true);
        $('#job-name').prop('readonly', true);

        orderForm.search_q.jobs = [];
        orderForm.search_q.employees = [];

        $('#job-search').keyup( function() {
            orderForm.search_q.jobs.push( $(this).val() );
            setTimeout( function() { orderForm.pop_q("jobs") }, 1000);
        });
        $('#employee-search').keyup( function() {
            orderForm.search_q.employees.push( $(this).val() );
            setTimeout( function() { orderForm.pop_q("employees") }, 1000);
        });




    }
};

$(orderFormAdmin.init);
