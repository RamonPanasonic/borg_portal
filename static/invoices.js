$(function() {
    get_data('/portal_proveedores/get');
});

function get_data(url) {
    // Mostrar el mensaje de carga
    $("#loadingMessage").show();

    // Realizar la llamada a la API para obtener los datos
    $.getJSON(url, function (data) {
        update_table(data.data);
        $("#loadingMessage").hide();
    });
}

function update_table(data) {
    let expense_concepts = [];
    $.each(data, function (i, element) {
        let expense_concept = [];
        expense_concept.push(element.id);
        expense_concept.push(element.name);
        expense_concept.push(element.invoice_date);
        expense_concept.push(element.invoice_date_due);
        expense_concept.push('$ ' + element.amount_total.toLocaleString("es-MX"));
        expense_concept.push(element.currency_id[1]);
        expense_concept.push('Aprobada')
        expense_concepts.push(expense_concept)
    });

    $('#datatable_list').DataTable().clear();
    $('#datatable_list').DataTable().destroy();
    $('#datatable_list').DataTable({
        dom: 'lBfrtip',
        "buttons": [
            'excel'
        ],
        responsive: true,
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json',
        },
        data: expense_concepts,
        columns: [
            {title: "ID"},
            {title: "Nombre"},
            {title: "Fecha de factura"},
            {title: "Fecha de pago"},
            {title: "Total"},
            {title: "Divisa"},
            {title: "Estado"}
        ]
    });
}

// Función para formatear el número con separadores de miles y decimales
function formatNumber(number) {
    return new Intl.NumberFormat('es-ES', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(number);
}
