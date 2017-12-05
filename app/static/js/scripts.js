var tablaFacturacion = $('#tabla-facturacion').DataTable({
	// paging: false,
	// searching: false,
	// ordering: false
});


// Imprime los números con formato 
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Añade una nueva fila
function addrow()
{

	$('tbody').append('<tr class="fila">'+
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

// Guarda los datos de la factura
$(document).ready(function()
{

	$('#guardar').click(function(event)
	{
		
		var fila = $('.fila').toArray();
		// console.log(fila.length)
		var arrayFilas = [];
		var cuenta = 0;
		var cuentaFilas = 1;
		var desc;
		var vUnitario;
		var cant;
		var pIva;
		var vIva;
		var totItem;
		var fil = 1
		
			while (cuenta < fila.length){
			var f = [];
			// console.log(fil, cuenta);
			desc = $('#tbl-fac-body tr:nth-child('+fil+')').find('#tr-descripcion').children().val();
			// console.log(desc, fil);
			vUnitario = $('#tbl-fac-body tr:nth-child('+fil+')').find('#tr-valUnitario').children().val();
			cant = $('#tbl-fac-body tr:nth-child('+fil+')').find('#tr-cantidad').children().val();
			pIva = $('#tbl-fac-body tr:nth-child('+fil+')').find('#tr-porcIva').children().val();
			vIva = $('#tbl-fac-body tr:nth-child('+fil+')').find('#tr-valIva').text();
			totItem = $('#tbl-fac-body tr:nth-child('+fil+')').find('#tr-valTotal').text();

			f[0] = desc;
			f[1] = vUnitario;	
			f[2] = cant;
			f[3] = pIva;
			f[4] = vIva;
			f[5] = totItem;
			
			arrayFilas.push(f);
			cuenta++;
			fil++;

		}



		function DatosFactura(numfactura, cliente, identificacion, direccion, ciudad, telefono, fecha, items, subtotal, iva, total){
			this.numfactura = numfactura;
			this.cliente = cliente;
			this.identificacion = identificacion
			this.direccion = direccion;
			this.ciudad = ciudad;
			this.telefono = telefono;
			this.fecha = fecha;
			this.items = items;
			this.subtotal = subtotal;
			this.iva = iva;
			this.total = total;
		};

	
	
		var data = new DatosFactura(
							$('#numero-factura').text(),
							$('#cliente').val(),
							$('#identificacion').val(),
							$('#direccion').val(),
							$('#ciudad').val(),				
							$('#telefono').val(),
							$('#fecha').val(),
							arrayFilas,
							$('#sumSubtotal').text(),
							$('#sumTotalIva').text(),
							$('#sumTotal').text(),
							)
		
		console.log(data);
 		
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
     		$('#successAlert').text(data.success).show();
                
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
