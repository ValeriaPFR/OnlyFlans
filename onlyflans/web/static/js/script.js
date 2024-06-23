//Funcionamiento del formulario de Registro de nuevo cliente

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("registroClienteForm").addEventListener("submit", function (event) {
        event.preventDefault();

        // Obtener los datos del formulario
        const name = document.getElementById("firstName").value;
        const lastname = document.getElementById("lastName").value;
        const email = document.getElementById("email").value;
        const birthDate = document.getElementById("birthDate").value;
        const address = document.getElementById("address").value;

        // Realizar la petición POST al backend de Django
        fetch("{% url 'new_client' %}", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": "{{ csrf_token }}"
            },
            body: JSON.stringify({
                email: email,
                name: name,
                lastname: lastname,
                birth_date: birthDate,
                address: address
            })
        })
            .then(response => {
                if (response.ok) {
                    // Redireccionar a la página de éxito o a donde sea necesario
                    window.location.href = "{% url 'new_client_success' %}";
                } else {
                    alert("Hubo un error al procesar tu solicitud. Por favor, intenta nuevamente.");
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("Hubo un error al procesar tu solicitud. Por favor, intenta nuevamente.");
            });
    });
});

//Funcionamiento del modal de login en el navbar
$(document).ready(function () {
    $('form').on('submit', function (e) {
        e.preventDefault();
        var email = $('#email').val();
        var password = $('#password').val();

        if (email && password) {
            // Aquí puedes agregar la lógica para el envío del formulario
            alert('Formulario enviado');
            $('#loginModal').modal('hide');
        } else {
            alert('Por favor, complete todos los campos');
        }
    });
});


