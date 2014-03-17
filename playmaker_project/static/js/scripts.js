$(document).ready(function() {

	// Make the sidebar's height match the content wrapper's height
	$(".uneven-heights").setAllToMaxHeight();

    // Adjust sidebar height
    var preferedHeight = $(window).height() - $(".header").css("height").slice(0,-2);
    $(".sidebar-wrap").css("height", preferedHeight);
    //$(".discussion").css("height", preferedHeight)

});

/*
 *	Helper methods
 *
 */

/*
 *	Make DIVs of the same height
 *	Usage: $(‘div.unevenheights’).setAllToMaxHeight();
 *  Thanks Paul Irish
 */

$.fn.setAllToMaxHeight = function(){
    console.log(this);
	return this.height(Math.max.apply(this,$.map(this,function(e){return $(e).height()})));
}