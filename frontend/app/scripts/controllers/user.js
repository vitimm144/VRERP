angular.module('frontendApp')
  .controller('MainCtrl', function (
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
    user_ctrl.gridOptions['data'] = response.data
  }, function(){
            console.log('erro ao pegar users');
  });
    
});

