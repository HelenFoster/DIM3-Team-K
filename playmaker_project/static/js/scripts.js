$(document).ready(function() {

    // Make the sidebar's height match the content wrapper's height
    $(".uneven-heights").setAllToMaxHeight();

    // Adjust sidebar height
    var preferedHeight = $(window).height() - $(".header").css("height").slice(0,-2);
    $(".sidebar-wrap").css("height", preferedHeight);

    // Set up mobile navigation menu
    $("#menu").mmenu({
        slidingSubmenus: false,
        classes: "mm-light"
    });

    // Trigger the menu on click
    $(".menu-mobile-button").click(function() {
        $("#menu").trigger( "open.mm" );
    });


});

/*
 *	Helper methods
 *
 */

/*
 *	Make DIVs of the same height
 *	Usage: $(‘div.unevenheights’).setAllToMaxHeight();
 *  Thanks @Paul Irish
 */

$.fn.setAllToMaxHeight = function(){
    return this.height(Math.max.apply(this,$.map(this,function(e){return $(e).height()})));
}

function reloadMessages(id, hostplayer) {

    var $target = $(".message-container");
    var url = "/getmsgs/" + id;

    // Retrieve all messages for the discussion
    $.getJSON(url).done(function(data) {

        $target.empty();
        var messages = [];

        // Process JSON into an array
        for (var i = 0; i < data.length; i++) {
            messages.push(data[i]);
        }

        // Append to the chat
        var output = [];
        $.each(messages, function() {

            var current = $(this)[0];

            if (hostplayer == current.user_op) {
                output.push('<li class="self">');
            } else {
                output.push('<li class="other">');
            }
            output.push('<div class="avatar"></div>');
            output.push('<div class="messages">');
            output.push('<p>' + current.message + '</p>');
            output.push('<time>' + current.user_op + ' • ' + current.time + ' ' + current.date + '</time>');
            output.push('</div></li>');

        });

        $target.append(output.join(''));
    }).fail(function() {
        alert("Could not reload messages!");
    });

}