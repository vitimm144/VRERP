angular.module('frontendApp')
  .controller('CareerEditCtrl', function (
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
  var career_edit_ctrl = this;
  career_edit_ctrl.url = 'api/careers/';
  console.log('stateParams');
  console.log($stateParams);
  
  if ($stateParams.careerId){
    console.log('career id ', $stateParams.careerId);
     
    $http.get(career_edit_ctrl.url  + $stateParams.careerId).then(function(data){
      console.log(data);
      career_edit_ctrl.career = data.data;
    });
  }else{
    career_edit_ctrl.career = {};
  }
  
  career_edit_ctrl.submit = function(){
    result = formService.saveFormData(career_edit_ctrl.career, career_edit_ctrl.url);
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



