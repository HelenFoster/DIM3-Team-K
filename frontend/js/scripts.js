$(document).ready(function() {

	// Make the sidebar's height match the content wrapper's height
	$(".uneven-heights").setAllToMaxHeight();


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
	return this.height(Math.max.apply(this,$.map(this,function(e){return $(e).height()})));
}