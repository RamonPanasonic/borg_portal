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
        if(element.x_studio_fecha_de_pago){
            expense_concept.push(element.x_studio_fecha_de_pago);
        }else{
            expense_concept.push('')
        }

        expense_concept.push('$ ' + element.amount_total.toLocaleString("es-MX", { minimumFractionDigits: 2, maximumFractionDigits: 2 }));
        expense_concept.push(element.currency_id[1]);
        if(element.x_studio_estado_de_pago){
            expense_concept.push(element.x_studio_estado_de_pago)
        }else{
            expense_concept.push('')
        }
        if(expense_concept.x_studio_estado_de_la_factura){
            expense_concept.push(element.x_studio_estado_de_la_factura)
        }else{
            expense_concept.push('')
        }

        expense_concepts.push(expense_concept)
    });

    $('#datatable_list').DataTable().clear();
    $('#datatable_list').DataTable().destroy();
    $('#datatable_list').DataTable({
    dom: 'lBfrtip',
    buttons: ['excel'],
    responsive: true,
    language: {
        url: 'https://cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json',
    },
    data: expense_concepts,
    columns: [
        { title: "ID" },
        { title: "Factura" },
        { title: "Fecha de factura" },
        { title: "Fecha estimada" },
        { title: "Total" },
        { title: "Divisa" },
        { title: "Estado de pago" },
        { title: "Estado de la factura" }
    ],
    createdRow: function(row, data, dataIndex) {
        $('td:eq(4)', row).css('text-align', 'right');
    },
    order: [[1, 'desc']]
});


}

// Función para formatear el número con separadores de miles y decimales
function formatNumber(number) {
    return new Intl.NumberFormat('es-ES', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(number);
}
