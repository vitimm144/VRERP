angular.module('frontendApp')
  .controller('StockCtrl', function (
  $rootScope,
  $scope,
  $http,
  $transitions,
  AuthService,
  gridService,
  AUTH_TOKEN_PATH,
  AUTH_LOGOUT_PATH
) {
  $rootScope.alertMessage = true;
  var stock_ctrl = this;
  var url = '/api/stocks';
  stock_ctrl.gridOptions = {};
  console.log('stock_ctrl');
  var update_grid = function(){
    var result = gridService.update_grid(url)
    result.then(
      function(response){
        stock_ctrl.stocks = response.data.results;
        console.log(stock_ctrl.stocks);
      }, function(){
        console.log('erro ao pegar stock');
      });
  } 
    
  update_grid();
  stock_ctrl.excluir = function(url){
   gridService.delete_data().then(
    function(){
      update_grid();
    }, function(){
      console.log('erro ao pegar stock');
    }); 
  }
  $transitions.onSuccess({}, function() {
    console.log('Transition on success');
    update_grid();
    
  });
    
});

