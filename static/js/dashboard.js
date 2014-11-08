$(document).ready(function() {

    // JQuery code to be added in here.

    //for the query-add button
    // $('.query-add').click(function(){
    //     var url = $(this).attr("url");
    //     var query = $(this).attr("query-str");
    //     var me = $(this);
    //     $.get(url + "?" + query, function(data){
    //         $('.sidebar').html(data);
    //         // $('.go_button').html(data);
    //         me.hide();
    //     });
    // });

    // click event of query-add
    $('.query-add').click(function(){
        // the href to display current state of dashboard
        var dash_href = $('#button-analyses-show').attr('href');

        // we will issue a GET to this url
        var sidebar_url = $(this).attr("data-sidebar-url");

        // stringyfied JSON data
        var query_to_add = $(this).attr("data-add-query")

        console.log(query_to_add)
        
        // need to make a copy for the callback later
        var me = $(this);

        // issue a GET to sidebar_url, with the ticker query
        $.get(sidebar_url, {ticker: query_to_add},
            function(data) {
                if (me.hasClass("btn-primary")){
                    // populate the addition
                    $('#sidebar-addition').html(data);

                    // change the addition name to flag it as populated 
                    $('#sidebar-addition').attr("id", "sidebar-addition-used");

                    // populate anoter addition div to be used next
                    $('.sidebar').append($('<div id="sidebar-addition"></div>'));

                    // change the button to success (green)
                    me.removeClass("btn-primary").addClass("btn-success");
                } else if (me.hasClass("btn-success")){
                    // without a store this removal is hard
                    // on click event iterate through the sidebar
                    // and remove the entry

                    // TODO : implement logic to update
                    
                    // change the button to primary (blue)
                    me.removeClass("btn-success").addClass("btn-primary");
                }
            });
    });
});

