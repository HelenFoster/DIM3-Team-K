$(document).ready(function() {

	// Make the sidebar's height match the content wrapper's height
	$(".uneven-heights").setAllToMaxHeight();

    // Adjust sidebar height
    var preferedHeight = $(window).height() - $(".header").css("height").slice(0,-2);
    $(".sidebar-wrap").css("height", preferedHeight);

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
    var url = "/getmsgs/1";
    var messages = [];

    // Retrieve all messages for the discussion
    $.get(url, {
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