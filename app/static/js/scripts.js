$(document).ready( function () 
{
    $('#tbl-itemsfactura').DataTable(
        {
            paging: false,
            searching: false,
            ordering: false,
            select: true,
            autoWidth: true,
        });
} );

$(document).ready(function()
{
    var t = $('#tbl-itemsfactura').DataTable();
    var counter = 2;
 
    $('#addRow').click(function() 
    {
        t.row.add( 
            $('<tr><td>counter</td><td><input class="input-sm" type="" name=""></td><td><input id="vlr-unitario" class="input-sm" type="" name=""></td><td><input id="cantidad" class="input-sm" type="" name=""></td><td><input id="prc-iva" class="input-sm" type="" name=""></td><td><input id="total" class="input-sm" type="" name=""></td></tr>') ).draw( false );
 
        counter++;
    } );
} );