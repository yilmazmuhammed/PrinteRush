let country_select = $("#country")
  .on('change', function(){
    set_city_options($(this).find(":selected").val());
});
let city_select = $("#city")
  .on('change', function(){
    set_district_options($(this).find(":selected").val());
});
let district_select = $("#district")
  .on('change', function(){
    set_visibility_address_detail();
});
let address_detail_input = $("#address_detail");
let invoice_type_radio = $("#invoice_type")
  .on('change', function(){
    set_visibility_invoice_information();
});
function   set_city_options(country_id){
  if(country_id === ''){
    city_select.parent().hide();
  }
  else {
    fetch(Flask.url_for("address_api_bp.cities_api", {"country_id": country_id})).then(function (response) {
      response.json().then(function (data) {
        if (data.result) {
          let cities = data.cities;
          let optionsHTML = "<option value=''>Sehir seçiniz...</option>";
          let i, city;
          for (i = 0; i < cities.length; i++) {
            city = cities[i];
            optionsHTML += "<option value='" + city.id + "'>" + city.city + "</option>";
          }
          city_select.html(optionsHTML);
        } else {
          city_select.html("<option value=''>" + data.err_msg + "</option>");
        }
        city_select.parent().show();
      });
    });
  }
}

function set_district_options(city_id){
  if(city_id === ''){
    district_select.parent().hide();
  }
  else {
    fetch(Flask.url_for("address_api_bp.counties_api", {"city_id": city_id})).then(function (response) {
      response.json().then(function (data) {
        if (data.result) {
          let counties = data.counties;
          let optionsHTML = "<option value=''>İlçe seçiniz...</option>";
          let i, district;
          for (i = 0; i < counties.length; i++) {
            district = counties[i];
            optionsHTML += "<option value='" + district.id + "'>" + district.district + "</option>";
          }
          district_select.html(optionsHTML);
        } else {
          district_select.html("<option value=''>" + data.err_msg + "</option>");
        }
        district_select.parent().show();
      });
    });
  }
}

function set_visibility_address_detail(){
    if(district_select.find(":selected").val() === ""){
      address_detail_input.parent().hide();
    } else {
      address_detail_input.parent().show();
    }
}

function set_visibility_invoice_type(){
  if($("#is_invoice_address").is(':checked')){
    invoice_type_radio.parent().show();
  } else {
    invoice_type_radio.parent().hide();
  }
}

function set_visibility_invoice_information(){
  let list = [$("#company_name"), $("#tax_number"), $("#tax_office")];
  let i;
  if($('input[name="invoice_type"]:checked').val() === "1"){
    for(i=0; i<list.length;i++){
      list[i].parent().hide();
      list[i].removeAttr('required');
    }
  } else {
    for(i=0; i<list.length;i++){
      list[i].parent().show();
      list[i].prop('required',true);
    }
  }
}

$(document)
  .ready(function () {
    set_city_options(country_select.find(":selected").val());
    set_district_options(city_select.find(":selected").val());
    set_visibility_address_detail();
    set_visibility_invoice_type();
    set_visibility_invoice_information();
  })
  .on('change', '#is_invoice_address', function(){
    set_visibility_invoice_type();
});
