'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the frontendApp
 */
angular.module('frontendApp')
  .controller('MainCtrl', function (
  $rootScope,
  $scope,
  $http,
  AuthService,
  AUTH_TOKEN_PATH,
  AUTH_LOGOUT_PATH) {
    var main = this;
    console.log('main ctrl');
    //function receive a callback as a parameter for execute any function that
    //user pass to it, and receive a array of parameters to be used in this 
    //callback
    $scope.loggedIn = true;
    
    $rootScope.$on('event:loginRequired', function(evt){
            console.log('rootenventLoginRequired');
      $scope.loggedIn = false;
    });
//    main.$on('event:loginRequired', function(evt){
//            console.log('main enventLoginRequired');
//      $scope.loggedIn = false;
//    });
    $scope.$on('event:loginRequired', function(evt){
            console.log('scope enventLoginRequired');
      $scope.loggedIn = false;
    });
       
  });
