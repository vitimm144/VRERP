angular.module('frontendApp')
  .controller('ProductEditCtrl', function (
//  $rootScope,
  $scope,
  $stateParams,
  $state,
  Upload,
  $http,
  AuthService,
  formService,
  alertService,
  AUTH_TOKEN_PATH,
  AUTH_LOGOUT_PATH
){
  var product_edit_ctrl = this;
  product_edit_ctrl.url = 'api/products/';
  console.log('stateParams');
  console.log($stateParams);
  
  product_edit_ctrl.sizes = [
    'PP',
    'P',
    'M',
    'G',
    'GG'
  ];
  
  if ($stateParams.productId){
    product_edit_ctrl.url += $stateParams.productId + '/';
    console.log('product id ', $stateParams.productId);
    product_edit_ctrl.method = 'PUT';
    $http.get(product_edit_ctrl.url).then(function(data){
      console.log(data);
      product_edit_ctrl.product = data.data;
    });
  }else{
    product_edit_ctrl.method = 'POST';
    product_edit_ctrl.product = {};
  }
  
  product_edit_ctrl.submit = function(file) {
    file.upload = Upload.upload({
      method : product_edit_ctrl.method,
      url: product_edit_ctrl.url,
      data: product_edit_ctrl.product,
      file:file,
      fileFormDataName: 'picture' 
    });

    file.upload.then(function (response) {
      var message = 'Operação realizada com sucesso';
      alertService.message(message, 'success');
      $state.go( '^' );
    }, function (response) {
      if (response.status > 0)
        $scope.errorMsg = response.status + ': ' + response.data;
        var message = 'Erro na operação'
        alertService.message(message, 'danger');
    }, function (evt) {
      // Math.min is to fix IE which reports 200% sometimes
      file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
    });
  };
  
//  product_edit_ctrl.submit = function(){
//    result = formService.saveFormData(product_edit_ctrl.product, product_edit_ctrl.url);
//    result.then(
//    function (response) {
////      window.alert('ok');
//      var message = 'Operação realizada com sucesso';
//      alertService.message(message, 'success');
//      $state.go( '^' );
//    }, function (response) {
//      var message = 'Erro na operação'
//      alertService.message(message, 'danger');
//    });
//  } 
});



