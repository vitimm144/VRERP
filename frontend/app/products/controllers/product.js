angular.module('frontendApp')
  .controller('ProductCtrl', function (
  $rootScope,
  $scope,
  $http,
  AuthService,
  gridService,
  AUTH_TOKEN_PATH,
  AUTH_LOGOUT_PATH
) {
  $rootScope.alertMessage = true;
  var product_ctrl = this;
  var url = '/api/products';
  product_ctrl.gridOptions = {};
  console.log('products_ctrl');
  var update_grid = function(){
    var result = gridService.update_grid(url)
    result.then(
      function(response){
        product_ctrl.products = response.data.results;
        console.log(product_ctrl.products);
      }, function(){
        console.log('erro ao pegar products');
      });
  } 
    
  update_grid();
  product_ctrl.excluir = function(url){
   gridService.delete_data().then(
    function(){
      update_grid();
    }, function(){
      console.log('erro ao pegar products');
    }); 
  }
  $rootScope.$on('$stateChangeSuccess', function(
    event, toState, toParams, fromState, fromParams
  ){
            console.log(toState);
    if (toState.url == '/products'){
      update_grid();
    }
  });
    
});

