angular.module('frontendApp')
  .controller('UserCtrl', function (
  $rootScope,
  $scope,
  $http,
  $transitions,
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
  $transitions.onSuccess({}, function() {
    console.log('Transition on success');
    update_grid();
    
  });
    
});

