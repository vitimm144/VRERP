angular.module('frontendApp')
  .controller('StockCtrl', function (
  $rootScope,
  $scope,
  $state,
  $http,
  $transitions,
  AuthService,
  gridService,
  AUTH_TOKEN_PATH,
  AUTH_LOGOUT_PATH
) {
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
  };
    
  update_grid();
  stock_ctrl.excluir = function(url){
   gridService.delete_data(url).then(
    function(){
      $state.transitionTo($state.current, {}, { reload: true });
    }, function(){
      console.log('erro ao pegar stock');
    }); 
  };
  
  stock_ctrl.edit = function(id){
    $state.go('stock.edit', {"stockId":id});
  };
  stock_ctrl.transfer = function(id){
    $state.go('stock.transfer', {"stockId":id});
  };
    
});

