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

    /* Displays proper fields based on if the items are going in or out
     */
    order_type_display: function() {
        var in_or_out = $('input[name="order-type"]:checked').val();
        if (in_or_out == "in") {
            $('#admin').hide();
            $('#order-info').hide();
            $('#message-area').hide();
        }
        else {
            $('#admin').show();
            $('#order-info').show();
            $('#message-area').show();
        }
    },

    /* Calls proper function based on if order is incoming or outgoing
     */
    submit_order: function() {
        var in_or_out = $('input[name="order-type"]:checked').val();

        if (in_or_out == "in") {
            var count = 0;
            for (id in orderForm.order.line_items) count++;

            if (count > 0) {
                Dajaxice.inventory.add_stock( Dajax.process, { order_json: JSON.stringify(orderForm.order) } );
                orderForm.order_complete();
            }
            else {
                alert('There are no items to submit');
            }
        }
        // outgoing order
        else {
            orderForm.submit_order();
        }
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

        $('#in-or-out').change( orderFormAdmin.order_type_display );
        orderFormAdmin.order_type_display();

        $('#job-search').keyup( function() {
            orderForm.search_q.jobs.push( $(this).val() );
            setTimeout( function() { orderForm.pop_q("jobs") }, 1000);
        });
        $('#employee-search').keyup( function() {
            orderForm.search_q.employees.push( $(this).val() );
            setTimeout( function() { orderForm.pop_q("employees") }, 1000);
        });

        $('#submit-order').unbind();
        $('#submit-order').click( orderFormAdmin.submit_order );

        // override orderForm.order_complete in order to expediate multiple orders
        orderForm.order_complete = function() {
            $('.row').html("<div class='hero-unit'><h1>Entry complete</h1><h3>Click <a href='/entry'>here</a> to make another entry</h3></div>");
        };
    }
};

$(orderFormAdmin.init);
