var cartButtons = document.querySelectorAll('.cartAddForm');

Array.prototype.forEach.call(cartButtons, function(button) {
    button.addEventListener('submit', function(event) {
        event.preventDefault();

        const form = event.target;
        const url = form.action;
        const formData = new FormData(form);

        fetch(url, {
            method: 'POST',
            headers: {'X-CSRFToken': formData.get('csrfmiddlewaretoken')},
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                var snackbar = document.getElementById("snackbar");
                snackbar.className = "show";
                snackbar.innerText  = "Товар в корзине!";
                setTimeout(function(){ 
                    snackbar.className = snackbar.className.replace("show", "");
                }, 3000);
            } 
            else {
                var snackbar = document.getElementById("snackbar");
                snackbar.className = "show";
                snackbar.innerText  = "При добавлении товара в корзину произошла ошибка!";
                setTimeout(function(){ 
                    snackbar.className = snackbar.className.replace("show", ""); 
                }, 3000);
            }
        })
        .catch(error => {
            console.error('Error', error)
        })
    });
});