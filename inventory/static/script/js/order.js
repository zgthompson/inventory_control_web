var orderForm = {

    /* This is the internal representation of the order.
     */
    order: { line_items: {} },

    /* Change the quantity of an item already added to the order.
     * This function changes the quanity to an edit text field.
     */
    edit_item: function(e) {
        // parent of parent is the row 
        var cur_row = e.parentElement.parentElement;
        // second child contains amount
        var amount = cur_row.children[1];
        amount.innerHTML = "<input type='text' value='" + amount.innerHTML + "'>";
        e.innerHTML = "Done";
        $(e).attr('onclick', 'orderForm.edit_done(this);');
    },

    /* When the quantity is changed, this function updates the internal
     * representation of the order. If the input is invalid (NaN or < 0)
     * than the change is ignored and the previous value is restored.
     */
    edit_done: function(e) {
        var cur_item = $(e).attr('data');
        // parent of parent is the row 
        var cur_row = e.parentElement.parentElement;
        // second child contains td, first child of td is input box
        var input_box = cur_row.children[1].children[0];
        var quantity = parseInt(input_box.value);
        if (!isNaN(quantity) && quantity >= 0) {
            if (quantity == 0) {
                delete orderForm.order.line_items[cur_item];
            }
            else {
                orderForm.order.line_items[cur_item].quantity = quantity;
            }
        }
        orderForm.display_items();
    },

    /* This function adds the amount specified of a particular item to the
     * order. If that item is already in the order, the amount specified is
     * added to the previous total.
     */
    add_item: function(e) {
        var cur_item = $(e).attr('data');
        // parent of parent is the row 
        var cur_row = e.parentElement.parentElement;
        // first child contains name
        var name = cur_row.children[0].innerHTML;
        // third child contains the units
        var units = cur_row.children[2].innerHTML;
        // second child contains input value
        var input_box = cur_row.children[1].children[0];
        var quantity = parseInt(input_box.value);
        if (!isNaN(quantity) && quantity > 0) {
            if ( orderForm.order.line_items.hasOwnProperty(cur_item) ) {
                orderForm.order.line_items[cur_item].quantity += quantity;
            }
            else {
                orderForm.order.line_items[cur_item] = {};
                orderForm.order.line_items[cur_item].name = name;
                orderForm.order.line_items[cur_item].quantity = quantity;
                orderForm.order.line_items[cur_item].units = units;
            }
            orderForm.display_items();
        }
        input_box.value = "";
    },

    /* This function adds a message to the pending order
     */
    add_message: function(e) {
        var out = "<textarea rows='10'></textarea><div><button class='btn' onclick='orderForm.display_message(this);'>Remove message</button>"
        $('#message').html(out);
    },

    /* This function generates the HTML markup for the pending order items
     * If there is no items in the order then the markup will specify that 
     * the order is empty.
     */
    display_items: function() {
        var out = "";

        // iterate over every line item and created a table row
        for (id in orderForm.order.line_items) {
            var item = orderForm.order.line_items[id];
            out += "<tr><td>" + item.name + "</td><td>" + item.quantity + "</td><td>" + item.units + "</td></td><td><button class='btn' data='" + id + "' onclick='orderForm.edit_item(this);'>Edit</button></td></tr>";
        }
        // if out is not empty
        if (out) {
            var table_front = "<table class='table table-condensed'><tr><th>Item</th><th>Amount</th><th>Units</th><th></th></tr>";
            var table_end = "</table>"
            out = table_front + out + table_end;
        }
        else {
            out = "<p>No items have been added</p>";
        }

        $('#pending-order').html(out);
    },

    /* This function generates the HTML markup for the order message based
     * on its current state (empty or not)
     */
    display_message: function() {
        var out;
        var message = orderForm.order.message;

        out = "<div><button class='btn' onclick='orderForm.add_message(this);'>Add message</button></div>";

        $('#message').html(out);
    },

    /* This array holds all the search queries made in the last second
     */
    search_q: { items: []  },

    /* This function will remove the oldest query from the search_q array. If
     * that query was the last element of the array, then an AJAX request is
     * made to update the displayed items to correspond to the query. The
     * purpose of this function is to delay an AJAX request until the user is
     * done typing their search, so as to not bombard the server on every
     * keydown.
     */
    pop_q: function(type) {
        var query = orderForm.search_q[type].shift();
        if (orderForm.search_q[type].length == 0) {
            eval("Dajaxice.inventory.search_" + type + "( Dajax.process, { query: query } );");
        }
    },

    /* Displays the order complete page
     */
    order_complete: function() {
        $('.row').html("<div class='hero-unit'><h1>Your order is complete</h1></div>");
    },
    /* This function submits the order to the backend and creates a new order
     * in the system
     */
    submit_order: function() {
        var employee_name = $('#employee-name').val();
        var job_name = $('#job-name').val();
        var message = $('#message textarea') ? $('#message textarea').val() : "";

        if ( !employee_name ) alert('You must enter the employee name');
        else if ( !job_name ) alert('You must enter the job name');
        else {
            var count = 0;
            for (id in orderForm.order.line_items) count++;
            if (count > 0 || message) {

                orderForm.order.employee_name = employee_name;
                orderForm.order.job_name = job_name;
                orderForm.order.message = message;
                Dajaxice.inventory.add_order( Dajax.process, { order_json: JSON.stringify(orderForm.order) } );
                orderForm.order_complete();
            }
            else {
                alert('There are no items or message to submit');
            }
        }
    },

    /* This function attaches a keydown listener on the search box,
     * an onclick listeer to the order submit button, and populates the
     * html for the empty order and message, and the add items
     */
    init: function() {
        $('#item-search').keyup( function() {
            orderForm.search_q.items.push( $(this).val() );
            setTimeout( function() { orderForm.pop_q("items") }, 1000);
        });
        $('#submit-order').click( orderForm.submit_order );
        orderForm.display_items();
        orderForm.display_message();
        Dajaxice.inventory.search_items( Dajax.process, { query: "" } );
    }
};

$(orderForm.init);
