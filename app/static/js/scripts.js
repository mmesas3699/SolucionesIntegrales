$(document).ready(function()
{
    $("#but").click(function()
    {
        $("#tbl-itemsfactura").hide();
    });
});

$(document).ready(function()
{
    $("#button").click(function()
    {
        var vrlUnitario = $("#vlr-unitario").val();
        var cantidad = $("#cantidad").val();
        var prcIva = $("#prc-iva").val();
        var totlSinIVa = vrlUnitario * cantidad
        var totlIVa = totlSinIVa * prcIva / 100
        $("#total").val(totlSinIVa + totlIVa);
    });
});