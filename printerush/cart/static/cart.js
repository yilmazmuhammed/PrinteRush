function show_message_modal(msg) {
  $('#message-modal').modal('show').children().children().children().text(msg);
}

function toggle_message_modal(msg) {
  $('#message-modal').modal('toggle').children().children().children().text(msg);
}

// async function add_to_cart2(product_id, quantity){
//   const response = await fetch(Flask.url_for("cart_api_bp.add_to_cart", {"product_id": product_id, "quantity": quantity}))
//   const data = await response.json();
//   let msg = "";
//   if(data.result){
//     msg = data.msg;
//   }
//   else{
//     msg = data.err_msg;
//   }
//   alert(msg);
//   return msg;
// }

async function api_add_to_cart(product_id, quantity){

  console.log(product_id + " " + quantity);
  const response = await fetch(Flask.url_for("cart_api_bp.add_to_cart", {"product_id": product_id, "quantity": quantity}));
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

async function api_remove_from_cart(product_id, quantity=0){
  const response = await fetch(Flask.url_for("cart_api_bp.remove_from_cart", {"product_id": product_id, "quantity": quantity}));
  const data = await response.json();
  let msg = "";
  if(data.result){
    msg = data.msg;
  }
  else{
    msg = data.err_msg;
  }
  // show_message_modal(msg);
}

async function api_update_cart_product(product_id, quantity){
  // // TODO translation ile yap
  // toggle_message_modal("Sepet güncelleniyor...");
  const response = await fetch(Flask.url_for("cart_api_bp.cart_product", {"product_id":product_id}));
  const data = await response.json();
  if(data.result){
    let cp = data.cart_product;
    let adding_quantity = quantity - cp.quantity;
    if(adding_quantity>0){
      await api_add_to_cart(product_id, adding_quantity);
      return cp.product_ref.main_option.price * quantity;
    }
  }
}

async function update_cart(){
  const response = await fetch(Flask.url_for("cart_api_bp.cart"));
  const data = await response.json();
  if(data.result){
    let cart_products = data.cart;
    let i=0, html="", cp, sum = 0;
    for(i=0; i < cart_products.length; i++){
      cp = cart_products[i]
      html += "<li id=\"up-cart-p\""+cp.product_ref.id+">\n" +
              "  <a id=\"remove-from-cart-p"+cp.product_ref.id+"\" class=\"btn btn-sm close-cart\"><i class=\"fa fa-times-circle\"></i></a>\n" +
              "  <div class=\"media\"> <a class=\"pull-left\"> <img alt=\"Everypick\" src=\""+cp.product_ref.main_photo.file_path+"\"></a>\n" +
              "    <div class=\"media-body\">\n" +
              "      <span><a href=\""+Flask.url_for("products_bp.view", {"product_id": cp.product_ref.id, "p":cp.product_ref.name})+"\">"+cp.product_ref.name+"</a></span>\n" +
              "      <div><span class=\"cart-price\">"+cp.product_ref.main_option.price+"</span> TL</div>\n" +
              "      <div class=\"product-qty\"><span>Adet:</span><span class=\"custom-qty\">"+cp.quantity+"</span></div>\n" +
              "    </div>\n" +
              "  </div>\n" +
              "</li>"
      sum += cp.product_ref.main_option.price*cp.quantity;
    }
    $(".cart-list").html(html);
    $(".cart-price-box.price-box").html(sum + "₺");
    $("#number-of-cart-product").html(i);
  }
}

async function update_cart_page_html(){
  const response = await fetch(Flask.url_for("cart_api_bp.cart"));
  const data = await response.json();
  if(data.result){
    let cart_products = data.cart;
    let i=0, html="", cp, total_price = 0;
    for(i=0; i < cart_products.length; i++){
      cp = cart_products[i]
      html += "<tr>\n" +
              "  <td><div class=\"product-image\">\n" +
              "    <a class=\"pull-left\" href=\""+Flask.url_for("products_bp.view", {"product_id": cp.product_ref.id, "p":cp.product_ref.name})+"\">\n" +
              "      <img alt=\"Everypick\" src=\""+cp.product_ref.main_photo.file_path+"\">\n" +
              "    </a>\n" +
              "  </div></td> \n" +
              "  <td><div class=\"product-title\"> \n" +
              "    <a href=\""+Flask.url_for("products_bp.view", {"product_id": cp.product_ref.id, "p":cp.product_ref.name})+"\">"+ cp.product_ref.name +"</a>\n" +
              "  </div></td>\n" +
              "  <td><ul><li><div class=\"base-price price-box\"> \n" +
              "    <span class=\"price\">"+ cp.product_ref.main_option.price +" ₺</span>\n" +
              "  </div></li></ul></td>\n" +
              "  <td><div class=\"input-box\"><div class=\"form-group\">\n" +
              "    <input id=\"cart-page-quantity-p"+ cp.product_ref.id +"\" class=\"form-control\" name=\"quantity_cart\" type=\"number\" style=\"max-width: 65px;border-radius: .40rem;\" value=\""+ cp.quantity +"\"/>\n" +
              "  </div></div></td>\n" +
              "  <td><div class=\"total-price price-box\"> \n" +
              "    <span class=\"price\">"+ cp.product_ref.main_option.price * cp.quantity +" ₺</span>\n" +
              "  </div></td>\n" +
              "  <td><div id=\"cart-page-remove-p"+ cp.product_ref.id +"\">\n" +
              "    <i title=\"Remove Item From Cart\" data-id=\"100\" class=\"fa fa-trash cart-remove-item\"></i>\n" +
              "  </div></td>\n" +
              "</tr>"
      total_price += cp.product_ref.main_option.price*cp.quantity;
      }
    $("#cart-body").html(html);
    $("#total-cart-price").html(total_price + "₺");
  }
}

$(document)
  .ready(function () {
    update_cart();
    update_cart_page_html();
  })
  .on('click', '[id^="remove-from-cart-p"]', function(){
    let product_id = this.id.substring(18);
    api_remove_from_cart(product_id).then(r => update_cart());
  })
  .on("click", '[id^="add-to-cart-p"]', function(){
    let product_id = this.id.substring(13);
    let quantity = $('#qty').val();
    api_add_to_cart(product_id, quantity).then(function (msg) {
      show_message_modal(msg);
      update_cart();
    });
  })
  .on("change", '[id^="cart-page-quantity-p"]', function () {
    let new_quantity = $(this).val();
    let product_id = this.id.substring("cart-page-quantity-p".length);
    api_update_cart_product(product_id, new_quantity).then(r => update_cart_page_html()).then(r => toggle_message_modal("Sepet güncellendi."));
  })
  .on("click", '[id^="cart-page-remove-p"]', function () {
    let product_id = this.id.substring("cart-page-remove-p".length);
    api_remove_from_cart(product_id).then(r => update_cart_page_html()).then(r => toggle_message_modal("Sepet güncellendi."));
  })
  .on("click", '[id^="wishlist-p"]', function(){
    alert("Beğendiklerime ekle");
  })
  .on("click", '[id^="compare-p"]', function(){
    alert("Karşılaştır");
  });