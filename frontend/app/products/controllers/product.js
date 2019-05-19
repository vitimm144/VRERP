angular.module('frontendApp')
  .controller('ProductCtrl', function (
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
  var product_ctrl = this;
  var url = '/api/products';
  
  $http.get('/api/colors').then(function(data){
    console.log(data);
    product_ctrl.colors = {};
    angular.forEach(data.data.results, function(color){
      product_ctrl.colors[color.id] = color;
    });
//    console.log(product_ctrl.colors);
  });
  
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
   gridService.delete_data(url).then(
    function(){
      $state.transitionTo($state.current, {}, { reload: true });
    }, function(){
      console.log('erro ao pegar products');
    }); 
  }
    
});

