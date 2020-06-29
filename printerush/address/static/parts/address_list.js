$(document)
  .on("click", ".address-card", function () {
    let prefix = $(this).attr("id").split("-")[0];
    let another_addresses = $("[id^='"+prefix+"'].address-card");
    another_addresses.removeClass("selected-card");
    another_addresses.children(".card-header").children("#check-icon").remove();
    $(this).addClass("selected-card");
    $(this).children(".card-header").append("<i id='check-icon' class='fa fa-check fa-2x ml-auto text-primary' aria-hidden='true' ></i>");
  })
  .on("click", '[id^="remove-address-"]', function () {
    let address_id = this.id.substring("remove-address-".length);
    fetch(Flask.url_for("address_api_bp.remove_address_api", {"address_id":address_id}));
    $(this).closest('.card').remove();
  });


function get_selected_address_id(prefix) {
  let selected_card = $("[id^='"+prefix+"'].selected-card");
  if(selected_card.length === 0)
    return 0;
  return parseInt(selected_card.attr('id').substring((prefix+"address-").length), 10);
}

modal_form_submit(function () {
  fetch(Flask.url_for("address_api_bp.get_last_address_api")).then(function (response) {
    response.json().then(function (data) {
      if(data.result) {
        let address = data.address;
        let prefix = $("#new-address-card").closest(".card-group").attr('id').split("-")[0]+"-";
        let html =  "<div id=\""+prefix+"address-"+ address.id +"\" class=\"card mx-1 my-2 address-card\" style=\"width: 18rem;\">\n" +
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
              "            <a id=\"remove-address-"+address.id+"\" class=\"card-link\">Sil</a>\n" +
              // "            <a href=\"#\" class=\"card-link\">Düzenle</a>\n" +
              "          </small>\n" +
              "        </div>\n" +
              "      </div>"
        $("#new-address-card").before(html);
      }
    });
  });
});