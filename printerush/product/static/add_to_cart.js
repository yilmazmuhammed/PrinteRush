function add_to_cart(product_id, quantity){
  fetch(Flask.url_for("cart_api_bp.add_product_to_cart", {"product_id": product_id, "quantity": quantity})).then(function(response) {
    response.json().then(function (data) {
      let msg = "";
      if(data.result){
        msg=data.msg;
      }
      else{
        msg=data.err_msg;
      }
      $('#message-modal').modal('show').children().children().children().text(msg);
    });
  });
}

$('[id^="compare-p"]').on("click", function(){
    alert("Karşılaştır");
});

$('[id^="add-to-cart-p"]').on("click", function(){
    let product_id = this.id.substring(13);
    let quantity = $('#qty').val();
    add_to_cart(product_id, quantity)
});


$('[id^="wishlist-p"]').on("click", function(){
      alert("Beğendiklerime ekle");
});