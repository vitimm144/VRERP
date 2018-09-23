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
    'ui.select',
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
//    var url_prefix = 'app/'
//    var url_prefix_2 = 'app/'
    var url_prefix = '../';
    var url_prefix_2 = '';
    $urlRouterProvider.otherwise( '/main' );
    $stateProvider
      .state('main', {
        url: '/main',
        views:{
          'content': {
            templateUrl: url_prefix_2 + 'views/main.html',
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
            templateUrl: url_prefix +  'products/views/products.html',
            controller: 'ProductCtrl',
            controllerAs: 'product_ctrl',
            authorize: true
          }
        }
      }).state('products.new', {
        url: '/new',
        views:{
          'form':{
            templateUrl: url_prefix + 'products/views/product_form.html',
            controller: 'ProductEditCtrl',
            controllerAs: 'product_edit_ctrl',
            authorize: true
          }
        }
      }).state('products.edit', {
        url: '/:productId',
        views:{
          'form':{
            templateUrl: url_prefix +  'products/views/product_form.html',
            controller: 'ProductEditCtrl',
            controllerAs: 'product_edit_ctrl',
            authorize: true
          }
        }
      })
      //SALES
      .state('sales', {
        url: '/sales',
        views:{
          'content': {
            templateUrl: url_prefix +  'sales/views/sales.html',
            controller: 'SaleCtrl',
            controllerAs: 'sale_ctrl',
            authorize: true
          }
        }
      }).state('sales.new', {
        url: '/new',
        views:{
          'form':{
            templateUrl: url_prefix + 'sales/views/sale_form.html',
            controller: 'SaleEditCtrl',
            controllerAs: 'sale_edit_ctrl',
            authorize: true
          }
        }
      }).state('sales.edit', {
        url: '/:saleId',
        views:{
          'form':{
            templateUrl: url_prefix +  'sales/views/sale_form.html',
            controller: 'SaleEditCtrl',
            controllerAs: 'sale_edit_ctrl',
            authorize: true
          }
        }
      })
      //EMPLOYEES
      .state('employees', {
        url: '/employees',
        views:{
          'content': {
            templateUrl: url_prefix +  'employees/views/employees.html',
            controller: 'EmployeeCtrl',
            controllerAs: 'employee_ctrl',
            authorize: true
          }
        }
      }).state('employees.new', {
        url: '/new',
        views:{
          'form':{
            templateUrl: url_prefix +  'employees/views/employee_form.html',
            controller: 'EmployeeEditCtrl',
            controllerAs: 'employee_edit_ctrl',
            authorize: true
          }
        }
      }).state('employees.edit', {
        url: '/:employeeId',
        views:{
          'form':{
            templateUrl: url_prefix +  'employees/views/employee_form.html',
            controller: 'EmployeeEditCtrl',
            controllerAs: 'employee_edit_ctrl',
            authorize: true
          }
        }
      })
      //CAREERS
      .state('careers', {
        url: '/careers',
        views:{
          'content': {
            templateUrl: url_prefix +  'careers/views/careers.html',
            controller: 'CareerCtrl',
            controllerAs: 'career_ctrl',
            authorize: true
          }
        }
      }).state('careers.new', {
        url: '/new',
        views:{
          'form':{
            templateUrl: url_prefix +  'careers/views/career_form.html',
            controller: 'CareerEditCtrl',
            controllerAs: 'career_edit_ctrl',
            authorize: true
          }
        }
      }).state('careers.edit', {
        url: '/:careerId',
        views:{
          'form':{
            templateUrl: url_prefix +  'careers/views/career_form.html',
            controller: 'CareerEditCtrl',
            controllerAs: 'career_edit_ctrl',
            authorize: true
          }
        }
      })
      //CLIENTS
      .state('clients', {
        url: '/clients',
        views:{
          'content': {
            templateUrl: url_prefix +  'clients/views/clients.html',
            controller: 'ClientCtrl',
            controllerAs: 'client_ctrl',
            authorize: true
          }
        }
      }).state('clients.new', {
        url: '/new',
        views:{
          'form':{
            templateUrl: url_prefix +  'clients/views/client_form.html',
            controller: 'ClientEditCtrl',
            controllerAs: 'client_edit_ctrl',
            authorize: true
          }
        }
      }).state('clients.edit', {
        url: '/:clientId',
        views:{
          'form':{
            templateUrl: url_prefix +  'clients/views/client_form.html',
            controller: 'ClientEditCtrl',
            controllerAs: 'client_edit_ctrl',
            authorize: true
          }
        }
      })
      //CLIENTS
      .state('stock', {
        url: '/stock',
        views:{
          'content': {
            templateUrl: url_prefix +  'stock/views/stock.html',
            controller: 'StockCtrl',
            controllerAs: 'stock_ctrl',
            authorize: true
          }
        }
      }).state('stock.new', {
        url: '/new',
        views:{
          'form':{
            templateUrl: url_prefix +  'stock/views/stock_form.html',
            controller: 'StockEditCtrl',
            controllerAs: 'stock_edit_ctrl',
            authorize: true
          }
        }
      }).state('stock.edit', {
        url: '/:stockId',
        views:{
          'form':{
            templateUrl: url_prefix + 'stock/views/stock_form.html',
            controller: 'StockEditCtrl',
            controllerAs: 'stock_edit_ctrl',
            authorize: true
          }
        }
      }).state('stock.transfer', {
        url: '/transfer/:stockId',
        views:{
          'form':{
            templateUrl: url_prefix + 'stock/views/stock_transfer.html',
            controller: 'StockTransferCtrl',
            controllerAs: 'stock_transfer_ctrl',
            authorize: true
          }
        }
      })
      //USERS
      .state('users', {
        url: '/users',
        views:{
          'content': {
            templateUrl: url_prefix_2 + 'views/users.html',
            controller: 'UserCtrl',
            controllerAs: 'user_ctrl',
            authorize: true
          }
        }
      }).state('users.new', {
        url: '/new',
        views:{
          'form':{
            templateUrl: url_prefix_2 + 'views/form.html',
            controller: 'UserEditCtrl',
            controllerAs: 'user_edit_ctrl',
            authorize: true
          }
        }
      }).state('users.edit', {
        url: '/:userId',
        views:{
          'form':{
            templateUrl: url_prefix_2 + 'views/form.html',
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
            templateUrl: url_prefix_2 + 'views/about.html',
            controller: 'AboutCtrl',
            authorize: true
          }
        }
      });
  })
  .constant( 'AUTH_TOKEN_PATH', '/api/auth/token/' )
  .constant( 'AUTH_LOGOUT_PATH', '/api/auth/logout/' );
