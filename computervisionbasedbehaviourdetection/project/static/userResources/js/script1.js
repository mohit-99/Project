$('.cardNumber').keyup(function () {
    var foo = $(this).val().split(" ").join(""); // remove hyphens
    if (foo.length > 0) {
        foo = foo.match(new RegExp('.{1,4}', 'g')).join(" ");
    }
    $(this).val(foo);
});