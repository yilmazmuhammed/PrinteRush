let params = new URLSearchParams(document.location.search.substring(1));

// redirect to url by sorting product
$("#my_sort").on('change', function () {
    params.set("sort", $(this).val());
    window.location.replace(location.pathname+"?"+params.toString());
}).val(params.get("sort") || "descending_sold");

// redirect to url by pagesize
$("#page-size").on('change', function () {
    params.delete("page");
    params.set("pagesize", $(this).val());
    window.location.replace(location.pathname+"?"+params.toString());
}).val(params.get("pagesize") || 24);

function price_range (min=0, max=1000) {
    let price_slider = $("#slider-range");
    let amount = $("#amount");
    price_slider.slider({
        range: true,
        min: min,
        max: max,
        values: [ params.get("min_price") || min, params.get("max_price") || max ],
        slide: function( event, ui ) {
            amount.val( ui.values[ 0 ] + "₺"  + " - " + ui.values[ 1 ] + "₺"  );
        }
    });
    amount.val( (params.get("min_price") || price_slider.slider( "values", 0 )) + "₺" + " - " + (params.get("max_price") || price_slider.slider( "values", 1 )) + "₺"  );
}

$("#refine").on("click", function () {
    let price_slider = $("#slider-range");
    params.set("min_price", price_slider.slider("values", 0));
    params.set("max_price", price_slider.slider("values", 1));
    params.set("min_point", ((parseInt($('input[name="product_point"]:checked').val()) || 1)-1).toString());
    window.location.replace(location.pathname+"?"+params.toString());
});

$("input[name=product_point][value=" + (parseInt(params.get("min_point"))+1) + "]").prop('checked', true);


function set_product_overview(product_id){
  fetch(Flask.url_for("product_api_bp.get_product_api", {"product_id":product_id})).then(function (response) {
    response.json().then(function (data) {
      if(data.result){
        let i, product = data.product;

        let photos_div = $("#popup_product_detail_photos_div")
        photos_div.html("");
        for(i=0; i<product.photos_set.length; i++){
          photos_div.append("<a href=\"#\"><img src=\""+product.photos_set[i].file_path+"\" alt=\""+product.name+"\"></a>")
        }

        $("#popup_product_detail_name").html(product.name);
        $("#popup_product_detail_point_div").html("<div title=\""+product.point+"\" class=\"rating-result\"> <span style=\"width:"+product.point*20+"%\"></span> </div>");
        $("#popup_product_detail_price_div").html("<span class=\"price\">"+product.main_option.price+"₺</span> <del class=\"price old-price\"></del>");
        $("#popup_product_detail_product_code").html(product.product_code);
        $("#popup_product_detail_short_description_div").html(product.short_description_html);
        $("#add-to-cart-btn-li").children().attr("id", "add-to-cart-p"+product_id);

        let stock_msg="";
        if(product.main_option.stock>0) stock_msg="Satışta";
        else stock_msg="Tükendi";
        $("#popup_product_detail_stock").html(stock_msg)
      }
    });
  });
}

$(document)
  .on("click", '[id^="product-overview-p"]', function() {
    let product_id = this.id.substring("product-overview-p".length);
    set_product_overview(product_id);
  });

