angular.module('frontendApp')
  .controller('ClientEditCtrl', function (
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
  var client_edit_ctrl = this;
  client_edit_ctrl.url = 'api/clients/';
  console.log('stateParams');
  console.log($stateParams);
  
  $http.get('/api/employees').then(function(data){
    
    console.log('employees');
    console.log(data);
    client_edit_ctrl.employees = data.data.results;
  });
  
  if ($stateParams.clientId){
    console.log('client id ', $stateParams.clientId);
     
    $http.get(client_edit_ctrl.url  + $stateParams.clientId).then(function(data){
      console.log(data);
      client_edit_ctrl.client = data.data;
    });
  }else{
    client_edit_ctrl.client = {};
  }
  
  client_edit_ctrl.submit = function(){
    result = formService.saveFormData(client_edit_ctrl.client, client_edit_ctrl.url);
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



