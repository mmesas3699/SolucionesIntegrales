var tablaFacturacion = $('#tabla-facturacion').DataTable({
	// paging: false,
	// searching: false,
	// ordering: false
});


// Añade una nueva fila
function addrow()
{

	$('tbody').append('<tr>'+
						'<td id="tr-descripcion"><input type="text" class="form-control input-sm"></td>'+
						'<td id="tr-valUnitario"><input type="text" class="valores unitario form-control input-sm"></td>'+
						'<td id="tr-cantidad"><input type="text" class="valores cantidad form-control input-sm"></td>'+
						'<td id="tr-porcIva"><input type="text"class="valores procIva form-control input-sm"></td>'+
						'<td id="tr-valIva" class="valIva"></td>'+
						'<td id="tr-valTotal" class="valTotal"></td>'+
					  '</tr>');
};


// Elimina la fila seleccionada
function removerow()
{
	$("tr.selected").remove();
};


// Imprime los números con formato 
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}


// Añade o quita la clase 'selected' para poder eliminar filas
$(document).ready(function()
{
    
    $('#tabla-facturacion tbody').on( 'click', 'tr', function ()
    {
        if ($(this).hasClass('selected'))
        {
            $(this).removeClass('selected');
        }
        else
        {
            $('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    });
});


// Calcula los valores de la factura
$(document).on('change', function()
{

	$('.valores').on('focusout', function()
	{

		var valUnitario = $(this).parents('tr').find('#tr-valUnitario').children().val();
		var cantidad =  $(this).parents('tr').find('#tr-cantidad').children().val();
		var porvIva = $(this).parents('tr').find('#tr-porcIva').children().val();
		var subTotalItem = valUnitario * cantidad
		var ivaItem = subTotalItem * porvIva / 100
		var totalItem = subTotalItem + ivaItem 
 		
 		$(this).parents('tr').find('#tr-valIva').text(ivaItem);
		$(this).parents('tr').find('#tr-valTotal').text(totalItem);


		// Para calcular los valores totales de los items y el IVA

		var sumTotal = 0
		var sumTotalIva = 0

		$('.valTotal').each(function()
		{
			sumTotal += parseInt($(this).text())
		});

		
		$('.valIva').each(function()
		{
			sumTotalIva += parseInt($(this).text())
		});

		var subTotal = sumTotal - sumTotalIva

		formatSubtotal = numberWithCommas(subTotal)
		formatSumTotal = numberWithCommas(sumTotal)
		formatSumTotalIva = numberWithCommas(sumTotalIva)

		$('#sumSubtotal').text(formatSubtotal)
		$('#sumTotal').text(formatSumTotal)
		$('#sumTotalIva').text(formatSumTotalIva)

		console.log(sumTotal, sumTotalIva)
	});
});

$(document).ready(function()
{

	$('#guardar').click(function(event)
	{
	
		function Datos(cliente, direccion, ciudad, telefono, fecha){
			this.cliente = cliente;
			this.direccion = direccion;
			this.ciudad = ciudad;
			this.telefono = telefono;
			this.fecha = fecha
		};
	
		var val = $('.valores');
		var fila = $('tr')

		var data = new Datos($('#cliente').val(),
							$('#direccion').val(),
							$('#ciudad').val(),				
							$('#telefono').val(),
							$('#fecha').val()
							)
		
		a = val[0]
		console.log(data, fila, fila.length);
 		
 		$.ajax(
 		{
   		url: '/guarda_factura',
   		type: 'POST',
   		contentType:'application/json',
   		data: JSON.stringify(data),
   		dataType:'json',
   		success: function(data)
   		{
     		//On ajax success do this
     		console.log(data.success);
      	},
   		error: function(xhr, ajaxOptions, thrownError)
   		{
      	//On error do this
        	if (xhr.status == 200)
        	{

            	alert(ajaxOptions);
        	}
        	else
        	{
            	alert(xhr.status);
            	alert(thrownError);
        	}
    	}
 		});
	});
});
