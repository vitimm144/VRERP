angular.module('frontendApp')
  .controller('UserEditCtrl', function (
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
  var user_edit_ctrl = this;
  user_edit_ctrl.url = 'api/users/';
  console.log('stateParams');
  console.log($stateParams);
  
  if ($stateParams.userId){
    console.log('user id ', $stateParams.userId);
     
    $http.get(user_edit_ctrl.url  + $stateParams.userId).then(function(data){
      console.log(data);
      user_edit_ctrl.user = data.data;
    });
  }else{
    user_edit_ctrl.user = {};
  }
  
  user_edit_ctrl.submit = function(){
    result = formService.saveFormData(user_edit_ctrl.user, user_edit_ctrl.url);
    result.then(
    function (response) {
//      window.alert('ok');
      var message = 'Operação realizada com sucsso';
      alertService.message(message, 'success');
      $state.go( '^', {},  {reload: true});
    }, function (response) {
      var message = 'Erro na operação'
      alertService.message(message, 'danger');
    });
  }; 
});



