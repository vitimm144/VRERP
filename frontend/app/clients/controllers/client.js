angular.module('frontendApp')
  .controller('ClientCtrl', function (
  $rootScope,
  $scope,
  $state,
//  $transition$,
  $http,
  AuthService,
  gridService,
  AUTH_TOKEN_PATH,
  AUTH_LOGOUT_PATH
) {
  $rootScope.alertMessage = true;
  var client_ctrl = this;
  var url = '/api/clients';
  client_ctrl.gridOptions = {};
  console.log('clients_ctrl');
  var update_grid = function(){
    var result = gridService.update_grid(url)
    result.then(
      function(response){
        client_ctrl.clients = response.data.results;
        console.log(client_ctrl.clients);
      }, function(){
        console.log('erro ao pegar clients');
      });
  }
  
  client_ctrl.edit = function(id){
    $state.go('clients.edit', {"clientId":id});
  }
    
  update_grid();
  client_ctrl.excluir = function(url){
   gridService.delete_data().then(
    function(){
      update_grid();
    }, function(){
      console.log('erro ao pegar clients');
    }); 
  }
//  $transition$.onSuccess(function(){
//            console.log('Success');
//  });
  $rootScope.$on('$stateChangeSuccess', function(
    event, toState, toParams, fromState, fromParams
  ){
            console.log('TOSTATE');
            console.log(toState);
    if (toState.url == '/clients'){
      update_grid();
    }
  });
    
});

