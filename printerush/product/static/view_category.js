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
    params.set("min_price", price_slider.slider( "values", 0 ));
    params.set("max_price", price_slider.slider( "values", 1 ));
    params.set("min_point", (parseInt($('input[name="product_point"]:checked').val())-1).toString());
    window.location.replace(location.pathname+"?"+params.toString());
});

$("input[name=product_point][value=" + (parseInt(params.get("min_point"))+1) + "]").prop('checked', true);


