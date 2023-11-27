$("form[name=signup_form]").submit(function (e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/signup",
        type: "POST",
        data: data,
        dataType: "json",
        success: function () {
            window.location.href = "/";
        },
        error: function (resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

$("form[name=login_form]").submit(function (e) {
    var $form = $(this);
    var data = $form.serialize();

    $.ajax({
        url: "/user/login",
        type: "POST",
        data: data,
        dataType: "json",
        success: function () {
            window.location.href = "/perfil/";
        },
        error: function (resp) {
            console.log(resp);
        }
    });

    e.preventDefault();
});
/*
$("form[name=task_form]").submit(function (e) {
    e.preventDefault();
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/add_task",
        type: "POST",
        data: data,
        dataType: "json",
        success: function () {
            var tasks = Task().get_user_tasks();
            updateTasksList(tasks);
            window.location.href = "/dashboard/";
        },
        error: function (resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

*/

$("form[name=task_form]").submit(function (e) {
    e.preventDefault();

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/add_task",
        type: "POST",
        data: data,
        dataType: "json",
        success: function () {
            window.location.href = "/dashboard/";
        },
        error: function (resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });
});

// Enviar el formulario de edición
$("#task_form").submit(function (e) {
    e.preventDefault();

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: $form.attr("action"),  // Usa la acción del formulario como URL
        type: "POST",
        data: data,
        dataType: "json",
        success: function () {
            // Actualiza la lista de tareas después de editar la tarea
            updateTasksList();
            // Limpia el formulario después de editar
            $form[0].reset();
        },
        error: function (resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });
});

// Función para eliminar una tarea
/*
function deleteTask(taskId) {
    $.ajax({
        url: "/delete_task",
        type: "POST",
        data: { task_id: taskId },
        dataType: "json",
        success: function (resp) {
            window.location.href = "/dashboard/";
        },
        error: function (resp) {
            console.log(resp);
        }
    });
}
*/
function deleteTask(taskId) {
    $.ajax({
        url: "/delete_task",
        type: "POST",
        data: { task_id: taskId },
        dataType: "json",
        success: function (resp) {
            // Actualiza la lista de tareas después de eliminar la tarea
            updateTasksList();
            //window.location.href = "/dashboard/";
        },
        error: function (resp) {
            console.log(resp);
        }
    });
}
// Función para actualizar la lista de tareas
function updateTasksList() {
    $.get("/dashboard/tasks", function (data) {
        var tasksList = $('.card ul');
        tasksList.empty();

        data.forEach(function (task) {
            var listItem =
                '<li>' +
                task.nombre + ' - ' + task.detalles + ' - ' + task.fecha_entrega +
                '<div>' +
                '<a href="#" class="btn btn-info btn-sm edit-btn" ' +
                'onclick="editTask(\'' + task._id + '\', \'' + task.nombre + '\', \'' + task.detalles + '\', \'' + task.fecha_entrega + '\')">Editar</a>' +
                '<a href="#" class="btn btn-danger btn-sm" onclick="deleteTask(\'' + task._id + '\')">Eliminar</a>' +
                '</div>' +
                '</li>';

            tasksList.append(listItem);
        });
    });
}
