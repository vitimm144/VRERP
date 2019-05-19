angular.module('frontendApp')
  .controller('UserCtrl', function (
  $rootScope,
  $scope,
  $http,
  $state,
  $transitions,
  AuthService,
  gridService,
  AUTH_TOKEN_PATH,
  AUTH_LOGOUT_PATH
) {
  $rootScope.alertMessage = false;
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
   gridService.delete_data(url).then(
    function(){
      $state.transitionTo($state.current, {}, { reload: true });
    }, function(){
      console.log('erro ao pegar users');
    }); 
  }
//  $scope.$on('event:loginConfirmed', function(evt){
//      $scope.loggedIn = true;
//  });
});

