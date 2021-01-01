function totPrice() {
    let price = Array.from(document.querySelectorAll('.price'));
    let quantity = Array.from(document.querySelectorAll('.quantity'));
    let total = 0;
    let i;
    for (i = 0; i < price.length; i++) {
        total += Number(price[i].innerHTML) * Number(quantity[i].innerHTML);
    }
    document.querySelector('#totalprice').innerHTML = total;
}
totPrice();