function checkForDelete() {
    var form = document.getElementById(`check-and-delete-form`);
    form.action = "/";
    form.method = "POST";
    form.submit();
}

function submitTable() {
    var form = document.getElementById(`table-form`);
    form.action = "/";
    form.method = "POST";
    form.submit();
}

function removeAll() {
    var confirmation = confirm('Continuing will remove all items from the list. OK?');
    if (confirmation === true) {
        var deletes = document.querySelectorAll('.deletebox');
        for (i in deletes) {
            deletes[i].checked = true;
        }
    } 
    submitTable();
}

function checkAll() {
    var checks = document.querySelectorAll('.checkbox');
    for (i in checks) {
        checks[i].checked = true;  
    }
    submitTable();
}