angular.module('frontendApp')
  .controller('SaleCtrl', function (
  $rootScope,
  $scope,
  $http,
  $transitions,
  AuthService,
  gridService,
  AUTH_TOKEN_PATH,
  AUTH_LOGOUT_PATH
) {
  
  var sale_ctrl = this;
  var url = '/api/sales';
  sale_ctrl.gridOptions = {};
  sale_ctrl.status = {
    "F":"Finalizada",
    "C":"Cancelada"
  }
  console.log('sales_ctrl');
  var update_grid = function(){
    var result = gridService.update_grid(url)
    result.then(
      function(response){
        sale_ctrl.sales = response.data.results;
        console.log(sale_ctrl.sales);
      }, function(){
        console.log('erro ao pegar sales');
      });
  } 
    
  update_grid();
  sale_ctrl.excluir = function(url){
   gridService.delete_data().then(
    function(){
      update_grid();
    }, function(){
      console.log('erro ao pegar sales');
    }); 
  }
  $transitions.onSuccess({}, function() {
    console.log('Transition on success');
    update_grid();
    
  });
  
    
});

