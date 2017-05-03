'use strict';

/**
 * @ngdoc overview
 * @name frontendApp
 * @description
 * # frontendApp
 *
 * Main module of the application.
 */
angular.module('frontendApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'frontendAuthApp',
    'ngTouch',
    'ui.router'
  ])
.run(function ($rootScope,AuthService) {
  console.log('run');
//  $rootScope.$on('$routeChangeStart', function (event, next, current) {
//    console.log('$routeChangeStart');
//    if (next.authorize) {
      if (!AuthService.getToken()) {
        console.log('No token');
        /* Ugly way
        event.preventDefault();
        $location.path('/login');
        ========================== */
        $rootScope.$broadcast('event:loginRequired');
        $rootScope.$emit('event:loginRequired');
      }
//    }
//  });

})
.config(function ($stateProvider, $urlRouterProvider  ) {
    $urlRouterProvider.otherwise( '/main' );
    $stateProvider
      .state('main', {
        url: '/main',
        views:{
          'content': {
            templateUrl: 'views/main.html',
            controller: 'MainCtrl',
            controllerAs: 'main',
            authorize: true
          }
        }
      })
      .state('users', {
        url: '/users',
        views:{
          'content': {
            templateUrl: 'views/users.html',
            controller: 'UserCtrl',
            controllerAs: 'user_ctrl',
            authorize: true
          }
        }
      })
      .state('about',{
        url: '/about',
        views:{
          'content': {
            templateUrl: 'views/about.html',
            controller: 'AboutCtrl',
            authorize: true
          }
        }
      });
  })
  .constant( 'AUTH_TOKEN_PATH', '/api/auth/token/' )
  .constant( 'AUTH_LOGOUT_PATH', '/api/auth/logout/' );
