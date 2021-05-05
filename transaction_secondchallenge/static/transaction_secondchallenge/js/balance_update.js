
//function fetch_data(){
//     var id = document.getElementById("user_id").innerHTML;
//     var url = "{% url 'transaction:details' ${id} %}"
//     var new_balance = document.getElementById("balance").innerHTML;
//     $.ajax({
//          url: url,
//          type: 'get',
//          success: function(data){
//               $("#balance").load(url + " #balance"); //must provide one space in-front of #balance in-order to work properly
//          },
//          complete:function(data){
//               setTimeout(fetch_data,4000);
//          }
//     });
//}
//$(document).ready(function(){
//    setTimeout(fetch_data,4000);
//});