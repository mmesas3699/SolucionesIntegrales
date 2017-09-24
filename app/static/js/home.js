$(document).ready(function()
{
    $('form').on('submit', function(event)
    {
        $.ajax({
            data : {
                username: $('#username').val(),
                email: $('#email').val(),
                message: $('#message').val()
            },
            type: 'POST',
            url: '/procesa_mensaje_contacto'
        }) 
        .done(function(data){
            if (data.error) {
                $('#errorAlert').text(data.error).show();
                $('#successAlert').hide();
            }
            else {
                $('#successAlert').text(data.success).show();
                $('#errorAlert').hide();
            }
        });
        event.preventDefault();
    });
});