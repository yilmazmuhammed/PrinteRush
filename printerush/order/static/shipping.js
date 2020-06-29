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