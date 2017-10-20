var tblItemsFactura = $('#tbl-itemsfactura').DataTable();

$(document).ready(function()
{
    var counter = 2;
 
    $('#addRow').click(function() 
    {
        tblItemsFactura.row.add( 
            $('<tr><td>counter</td><td><input class="input-sm" type="" name=""></td><td><input id="vlr-unitario" class="input-sm" type="" name=""></td><td><input id="cantidad" class="input-sm" type="" name=""></td><td><input id="prc-iva" class="input-sm" type="" name=""></td><td><input id="total" class="input-sm" type="" name=""></td></tr>') ).draw( false );
 
        counter++;
    } );
} );