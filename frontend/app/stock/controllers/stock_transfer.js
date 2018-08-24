angular.module('frontendApp')
  .controller('StockTransferCtrl', function (
//  $rootScope,
  $scope,
  $stateParams,
  $state,
  $http,
  AuthService,
  formService,
  alertService,
  AUTH_TOKEN_PATH,
  AUTH_LOGOUT_PATH
){
  var stock_transfer_ctrl = this;
  stock_transfer_ctrl.post_url = 'api/stock/transfer/';
  stock_transfer_ctrl.url = 'api/stocks/';
  stock_transfer_ctrl.post_data = {};
  
  console.log('stateParams');
  console.log($stateParams);
  stock_transfer_ctrl.stockId = $stateParams.stockId;
  console.log('stock id ', stock_transfer_ctrl.stockId);
  $http.get('/api/users').then(function(data){
    console.log(data);
    stock_transfer_ctrl.users = data.data.results;
  });
  
  $http.get('/api/products').then(function(data){
    console.log(data);
    stock_transfer_ctrl.products = data.data.results;
  });
  
  stock_transfer_ctrl.url += stock_transfer_ctrl.stockId + '/';
  $http.get(stock_transfer_ctrl.url).then(function(data){
    stock_transfer_ctrl.post_data.stock = data.data;   
    stock_transfer_ctrl.stock = data.data;
    
  });
  
  stock_transfer_ctrl.submit = function(){
    stock_transfer_ctrl.post_data['from_transfer'] = stock_transfer_ctrl.stock
    $http.post(stock_transfer_ctrl.post_url, stock_transfer_ctrl.post_data).then(
      function (response) {
        var message = 'Operação realizada com sucesso';
        alertService.message(message, 'success');
        $state.go( '^' );
      }, function (response) {
        var message = 'Erro na operação'
        alertService.message(message, 'danger');
      }
    );
  } 
  
});



