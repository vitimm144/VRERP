angular.module('frontendApp')
  .controller('UserCtrl', function (
  $rootScope,
  $scope,
  $http,
  AuthService,
  gridService,
  AUTH_TOKEN_PATH,
  AUTH_LOGOUT_PATH
) {
  $rootScope.alertMessage = true;
  var user_ctrl = this;
  var url = '/api/users';
  user_ctrl.gridOptions = {};
  console.log('user_ctrl');
  var update_grid = function(){
    var result = gridService.update_grid(url)
    result.then(
      function(response){
        user_ctrl.users = response.data.results;
        console.log(user_ctrl.users);
      }, function(){
        console.log('erro ao pegar users');
      });
  } 
    
  update_grid();
  user_ctrl.excluir = function(url){
   gridService.delete_data().then(
    function(){
      update_grid();
    }, function(){
      console.log('erro ao pegar users');
    }); 
  }
  $rootScope.$on('$stateChangeSuccess', function(
    event, toState, toParams, fromState, fromParams
  ){
            console.log(toState);
    if (toState.url == '/users'){
      update_grid();
    }
  });
    
});

