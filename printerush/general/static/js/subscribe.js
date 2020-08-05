async function api_add_subscribe(email){
  const response = await fetch(Flask.url_for("general_api_bp.subscribe_api", {"email": email}));
  const data = await response.json();
  let msg = "";
  if(data.result){
    msg = data.msg;
  }
  else{
    msg = data.err_msg;
  }
  return msg;
}


function validateEmail(email) {
  var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  return regex.test(email);
}

$(document)
  .on("click", '#subscribe_submit', function(){
    let email = $('#subscribe_email');
    if(validateEmail(email.val())) {
      api_add_subscribe(email.val()).then(function (msg) {
        show_message_modal(msg);
        email.val("");
      });
    }
    else{
      show_message_modal("Geçersiz mail");
    }
  })