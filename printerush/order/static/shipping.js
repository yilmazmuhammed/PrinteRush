modal_form_submit(function () {
  fetch(Flask.url_for("address_api_bp.get_last_address_api")).then(function (response) {
    response.json().then(function (data) {
      if(data.result) {
        let address = data.address;
        let html =  "<div id=\"address-"+ address.id +"\" class=\"card mx-1 my-2\" style=\"width: 18rem;\">\n" +
              "        <div class=\"card-header d-flex\">\n" +
              "          <h5 class=\"card-title\">"+ address.title +"</h5>\n" +
              "        </div>\n" +
              "        <div class=\"card-body\">\n" +
              "          <p class=\"card-text\">"+ address.first_name +" "+ address.last_name +"</p>\n" +
              "          <p class=\"card-text\">"+ address.address_detail +"</p>\n" +
              "          <p class=\"card-text\">"+ address.district_ref.district +"/"+ address.district_ref.city_ref.city +"/"+ address.district_ref.city_ref.country_ref.country +"</p>\n" +
              "          <p class=\"card-text\">"+ address.phone_number +"</p>\n" +
              "        </div>\n" +
              "        <div class=\"card-footer\">\n" +
              "          <small class=\"text-muted\">\n" +
              "            <a href=\"#\" class=\"card-link\">Sil</a>\n" +
              "            <a href=\"#\" class=\"card-link\">Düzenle</a>\n" +
              "          </small>\n" +
              "        </div>\n" +
              "      </div>"
        $("#address-0").before(html);
      }
    });
  });
});

$("#also_invoicing_address").on("click", function () {
  if($(this).is(':checked')){
    $("#invoicing-addresses").hide();
  }
  else{

    $("#invoicing-addresses").show();
  }
});

$("#continue").on("click", function () {

  let ia_id, sa_id = get_selected_address_id("shipping-");
  if($("#also_invoicing_address").is(':checked'))
    ia_id = sa_id;
  else
    ia_id = get_selected_address_id("invoicing-");

  $("#shipping_address").val(sa_id);
  $("#invoicing_address").val(ia_id);
  $("#form-shipping-address").submit();
});