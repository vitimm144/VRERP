angular.module('frontendApp')
  .controller('ColorEditCtrl', function (
//  $rootScope,
//  $scope,
  $stateParams,
  $state,
  $http,
  AuthService,
  formService,
  alertService,
  AUTH_TOKEN_PATH,
  AUTH_LOGOUT_PATH
){
  var color_edit_ctrl = this;
  color_edit_ctrl.url = 'api/colors/';
  console.log('stateParams');
  console.log($stateParams);
  
  if ($stateParams.colorId){
    console.log('color id ', $stateParams.colorId);
     
    $http.get(color_edit_ctrl.url  + $stateParams.colorId).then(function(data){
      console.log(data);
      color_edit_ctrl.color = data.data;
    });
  }else{
    color_edit_ctrl.color = {};
  }
  
  color_edit_ctrl.submit = function(){
    result = formService.saveFormData(color_edit_ctrl.color, color_edit_ctrl.url);
    result.then(
    function (response) {
//      window.alert('ok');
      var message = 'Operação realizada com sucesso';
      alertService.message(message, 'success');
      $state.go( '^', {},  {reload: true});
    }, function (response) {
      var message = 'Erro na operação'
      alertService.message(message, 'danger');
    });
  }; 
});



