angular.module('frontendApp')
  .controller('UserCtrl', function (
  $rootScope,
  $scope,
  $http,
  AuthService,
  AUTH_TOKEN_PATH,
  AUTH_LOGOUT_PATH
) {

  var user_ctrl = this;
  console.log('user_ctrl');
  user_ctrl.gridOptions = {};
  $http.get('/api/users').then(function(response){
    user_ctrl.users = response.data.results;
    console.log(user_ctrl.users);
  }, function(){
            console.log('erro ao pegar users');
  });
    
});

