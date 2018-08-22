angular.module('frontendApp')
  .controller('StockEditCtrl', function (
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
  var stock_edit_ctrl = this;
  stock_edit_ctrl.base_url = 'api/stocks/';
  stock_edit_ctrl.url = 'api/stocks/';
  
  console.log('stateParams');
  console.log($stateParams);
  
  $http.get('/api/users').then(function(data){
    console.log(data);
    stock_edit_ctrl.users = data.data.results;
  });
  
  $http.get('/api/products').then(function(data){
    console.log(data);
    stock_edit_ctrl.products = data.data.results;
  });
  
  if ($stateParams.stockId){
    stock_edit_ctrl.url += $stateParams.stockId + '/';
    stock_edit_ctrl.method = 'PUT';
    console.log(stock_edit_ctrl.url);
    $http.get(stock_edit_ctrl.url).then(function(data){
      
      stock_edit_ctrl.stock = data.data;
      console.log('edição');
      console.log(stock_edit_ctrl.stock);
    });
  }else{
    stock_edit_ctrl.method = 'POST';
    stock_edit_ctrl.stock = {
      "user":{},
      "product":{}
    };
  }
  
  stock_edit_ctrl.submit = function(){
    result = formService.saveFormData(stock_edit_ctrl.stock, stock_edit_ctrl.base_url);
    result.then(
    function (response) {
//      window.alert('ok');
      var message = 'Operação realizada com sucesso';
      alertService.message(message, 'success');
      $state.go( '^' );
    }, function (response) {
      var message = 'Erro na operação'
      alertService.message(message, 'danger');
    });
  } 
  
});



