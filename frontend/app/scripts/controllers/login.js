'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the frontendApp
 */
angular.module('frontendApp')
  .controller('LoginCtrl', function (
  $rootScope,
  $scope,
  $http,
  AuthService,
  AUTH_TOKEN_PATH,
  AUTH_LOGOUT_PATH) {
    var login_ctrl = this;
    $scope.loggedIn = true;
    $rootScope.alertMessage = false;
    console.log('login ctrl');
    //function receive a callback as a parameter for execute any function that
    //user pass to it, and receive a array of parameters to be used in this 
    //callback
    
    $scope.$on('event:loginConfirmed', function(evt){
      console.log('enventLoginConfirmed');
      $scope.loggedIn = true;
      
    });
//    login_ctrl.$on('event:loginRequired', function(evt){
//            console.log('login_ctrl enventLoginRequired');
//      $scope.loggedIn = false;
//    });
    $scope.$on('event:loginRequired', function(evt){
      console.log('scope enventLoginRequired');
      $scope.loggedIn = false;
      $rootScope.loggedIn = false;
      AuthService.setToken( '' );
    });
    login_ctrl.user = {
      username : AuthService.getUserName()
    }
     
    
    login_ctrl.login = function(callback, param){
      //added specific config to login requests 
      var config = {ignoreAuthModule: true};
            console.log('login');
      // Now, we need to get a token from the backend
      $http.post(AUTH_TOKEN_PATH, login_ctrl.user, config )
        .then(function(data){
                      console.log(data.data);
                      console.log(data.status);
        if(data.status === 200 && data.data.token){
          
          //starting event to unlock app
//          authService.loginConfirmed(data);
          //saving user session
//          cookieStorage.setCookie( 'username', $scope.user.username, 28800 );
          $rootScope.$broadcast('event:loginConfirmed');
              console.log('success');
              console.log(data);
          AuthService.setToken( data.data.token );
          AuthService.setUserName( login_ctrl.user.username );

          //Getting user permissions.
//          UserPermissions.get( $scope.user.username );

          //optional callback to execute anything  
//          if (callback) {
//            callback(param);
//          }
        }
      });
    };
    login_ctrl.logout = function(callback, param){
      $http.get(AUTH_LOGOUT_PATH).then(function(){
        $rootScope.$broadcast('event:loginRequired');
//        if ( $state && $state.$current.name ) {
//          $state.reload( $state.$current.name );
//        }
//        if (callback) {
//          callback(param);
//        }
      });
    }
  });

