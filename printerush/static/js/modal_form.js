$(function() {
  function after_form_submitted(data) {
    if(data.result)
    {
      $('[name^="modal-form-"]').hide();
      $('[name^="modal-form-"]').find("input[type=text], textarea, select, input[type=tel]").val("");
      $('#success_message').append("<div class=\"alert alert-success\" role=\"alert\"><h3>"+data.msg+"</h3></div>").show();
      $('#error_message').hide();
    }
    else
    {
      $('#error_message').append('<div class="alert alert-danger" role="alert"><h3>Hata</h3><ul></ul></div>');

      if(data.validate_on_submit){
        $('#error_message ul').append('<li>'+data.err_msg+'</li>');
      }
      else {
        jQuery.each(data.errors,function(key, val){
          $('#error_message ul').append('<li>'+val+'</li>');
        });
      }

      $('#success_message').hide();
      $('#error_message').show();

    }//else
  }

	$('[name^="modal-form-"]').submit(function(e){
    e.preventDefault();
    $('#success_message').html("");
    $('#error_message').html("");

    $form = $(this).show();

    $.ajax({
      type: "POST",
      url: document.location.pathname,
      data: $form.serialize(),
      success: after_form_submitted,
      dataType: 'json'
    });

  });
});

$('#form-modal').on("show.bs.modal", function(){
  $('[name^="modal-form-"]').show();
  $('#success_message').html("").hide();
  $('#error_message').html("").hide();
  $(this).closest('form').find("input[type=text]").val("");
});