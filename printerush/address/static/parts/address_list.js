$(document).on("click", ".card", function () {
  let prefix = $(this).attr("id").split("-")[0];
  $("[id^='"+prefix+"'].card").removeClass("selected-card");
  $("[id^='"+prefix+"'].card").children(".card-header").children("#check-icon").remove();
  $(this).addClass("selected-card");
  $(this).children(".card-header").append("<i id='check-icon' class='fa fa-check fa-2x ml-auto text-primary' aria-hidden='true' ></i>");
});


function get_selected_address_id(prefix) {
  let selected_card = $("[id^='"+prefix+"'].selected-card");
  if(selected_card.length === 0)
    return 0;
  return parseInt(selected_card.attr('id').substring((prefix+"address-").length), 10);
}