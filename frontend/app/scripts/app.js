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
//    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'frontendAuthApp',
    'ngTouch',
    'ui.router',
    'ngFileUpload',
    'datatables'
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
      //PRODUCTS
      .state('products', {
        url: '/products',
        views:{
          'content': {
            templateUrl: '../products/views/products.html',
            controller: 'ProductCtrl',
            controllerAs: 'product_ctrl',
            authorize: true
          }
        }
      }).state('products.new', {
        url: '/new',
        views:{
          'form':{
            templateUrl: '../products/views/product_form.html',
            controller: 'ProductEditCtrl',
            controllerAs: 'product_edit_ctrl',
            authorize: true
          }
        }
      }).state('products.edit', {
        url: '/:productId',
        views:{
          'form':{
            templateUrl: '../products/views/product_form.html',
            controller: 'ProductEditCtrl',
            controllerAs: 'product_edit_ctrl',
            authorize: true
          }
        }
      })
      //CAREERS
      .state('careers', {
        url: '/careers',
        views:{
          'content': {
            templateUrl: '../careers/views/careers.html',
            controller: 'CareerCtrl',
            controllerAs: 'career_ctrl',
            authorize: true
          }
        }
      }).state('careers.new', {
        url: '/new',
        views:{
          'form':{
            templateUrl: '../careers/views/career_form.html',
            controller: 'CareerEditCtrl',
            controllerAs: 'career_edit_ctrl',
            authorize: true
          }
        }
      }).state('careers.edit', {
        url: '/:careerId',
        views:{
          'form':{
            templateUrl: '../careers/views/career_form.html',
            controller: 'CareerEditCtrl',
            controllerAs: 'career_edit_ctrl',
            authorize: true
          }
        }
      })
      //USERS
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
      }).state('users.new', {
        url: '/new',
        views:{
          'form':{
            templateUrl: 'views/form.html',
            controller: 'UserEditCtrl',
            controllerAs: 'user_edit_ctrl',
            authorize: true
          }
        }
      }).state('users.edit', {
        url: '/:userId',
        views:{
          'form':{
            templateUrl: 'views/form.html',
            controller: 'UserEditCtrl',
            controllerAs: 'user_edit_ctrl',
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
