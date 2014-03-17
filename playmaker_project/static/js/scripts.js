$(document).ready(function() {

	// Make the sidebar's height match the content wrapper's height
	$(".uneven-heights").setAllToMaxHeight();

    // Adjust sidebar height
    var preferedHeight = $(window).height() - $(".header").css("height").slice(0,-2);
    $(".sidebar-wrap").css("height", preferedHeight);

    // Send messages via AJAX
    $(".chat-message-send").click(function() {

        var message = $(".chat-message").val();

        // TODO: pick up CSRF token and ship it along with ajax request
        if (message.trim() != "") {

            $.post("/sendmsg/", {
                data: message
            }).done(function() {
                alert("Message sent successfully!");
                reloadMessages();
            }).fail(function() {
                alert("Message sending failure!");
            });
        }

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

function reloadMessages() {

    var $target = $(".discussion");
    var url = "/getmessages/";
    var messages = [];

    // Retrieve all messages for the discussion
    $.post(url, {
        sessionId: "1"
    }).done(function(data) {
        alert("Successfully got the messages! ");

        // Clear current messages
        $target.empty();

        // Load the new messages
        $target.append(data);
    }).fail(function() {
        alert("Could not reload messages!");
    });

}