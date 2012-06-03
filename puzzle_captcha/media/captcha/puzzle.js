(function($) {

function updatePuzzleOutput(root) {
    if (!root) root = '.puzzle';
    var output = $('#puzzle_key').val();
    $(root + ' .piece input').each(function() {
        output += ',' + $(this).attr('name');
    });
    $('#puzzle_captcha_output').val(output);
}

$.fn.swap = function(b){
    // method from: http://blog.pengoworks.com/index.cfm/2008/9/24/A-quick-and-dirty-swap-method-for-jQuery
    b = $(b)[0];
    var a = this[0];
    var t = a.parentNode.insertBefore(document.createTextNode(''), a);
    b.parentNode.insertBefore(a, b);
    t.parentNode.insertBefore(b, t);
    t.parentNode.removeChild(t);
    return this;
};

$(document).ready(function() {
    updatePuzzleOutput();

    $( '.piece' ).draggable({
        revert: false,
        helper: function(){
            return $(this).children('img').clone();
        }//, containment: 'parent'
    });

    $( '.piece' ).droppable({
        accept: '.piece',
        tolerance: 'pointer',

        drop: function( event, ui ) {

            var draggable = ui.draggable, droppable = $(this),
                dragPos = draggable.position(), dropPos = droppable.position();
            
            draggable.css({
                left: dropPos.left+'px',
                top: dropPos.top+'px'
            });

            droppable.css({
                left: dragPos.left+'px',
                top: dragPos.top+'px'
            });
            draggable.swap(droppable);
            updatePuzzleOutput();
        }
    });

});

})(jQuery)
