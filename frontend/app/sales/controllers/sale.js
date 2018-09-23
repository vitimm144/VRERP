angular.module('frontendApp')
  .controller('SaleCtrl', function (
  $rootScope,
  $scope,
  $http,
  AuthService,
  gridService,
  AUTH_TOKEN_PATH,
  AUTH_LOGOUT_PATH
) {
  $rootScope.alertMessage = true;
  
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
  $rootScope.$on('$stateChangeSuccess', function(
    event, toState, toParams, fromState, fromParams
  ){
            console.log(toState);
    if (toState.url == '/sales'){
      update_grid();
    }
  });
  
    
});

