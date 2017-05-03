angular.module('frontendAuthApp', ['ngStorage',])
.factory('AuthService', function ($localStorage, $q) {
  return {
    getToken : function () {
              console.log('get token');
      return $localStorage.token;
    },
    setToken: function (token) {
              console.log('set token');
      $localStorage.token = token;
    },
    setUserName: function (user) {
      $localStorage.user = user;
    },
    getUserName : function () {
      return $localStorage.user;
    },
//    signin : function (data) {
//      $http.post('api/auth/token', data);
//    },
//    signup : function (data) {
////      $http.post('api/signup', data);
//    },
    logout : function (data) {
      delete $localStorage.token;
      $q.when();
    }
  };
})
.factory('AuthInterceptor', function ($rootScope, AuthService, $q) {
  return {
    request: function(config) {
      config.headers = config.headers || {};

      if (AuthService.getToken()) {
        config.headers['Authorization'] = 'Token ' + AuthService.getToken();
      }

      return config;
    },

    responseError: function(response) {
      if (response.status === 401 || response.status === 403) {
        $rootScope.$broadcast('event:loginRequired');
//        $location.path('/signin');
      }
              console.log('Response error ' + response.status);
      return $q.reject(response);
    }
  }
});

angular.module('frontendApp')
.config(function($httpProvider) {
  $httpProvider.interceptors.push('AuthInterceptor');
});


////var app = angular.module('frontendApp');
///* 
// * To change this license header, choose License Headers in Project Properties.
// * To change this template file, choose Tools | Templates
// * and open the template in the editor.
// */
//
//
//
//app.factory('AuthService', function AuthService ( $localStorage, $q) {
//  return {
//    getToken : function () {
//      return $localStorage.token;
//    },
//    setToken: function (token) {
//      $localStorage.token = token;
//    },
////    signin : function (data) {
////      $http.post('api/auth/token', data);
////    },
////    signup : function (data) {
////      $http.post('api/auth/logout', data);
//    },
//    logout : function (data) {
//      delete $localStorage.token;
//      $q.when();
//    }
//  };
//});
//
//app.factory('AuthInterceptor', function AuthInterceptor (
//  $rootScope,
//  $location,
//  AuthService,
//  $q
//) {
//  return {
//    request: function(config) {
//      config.headers = config.headers || {};
//
//      if (AuthService.getToken()) {
//        config.headers['Authorization'] = AuthService.getToken();
//      }
//
//      return config;
//    },
//
//    responseError: function(response) {
//      if (response.status === 401 || response.status === 403) {
//        $rootScope.$broadcast('event:loginRequired');
////        $location.path('/signin');
//      }
//
//      return $q.reject(response);
//    }
//  };
//});
//
//app.config(function($httpProvider) {
//  $httpProvider.interceptors.push('AuthInterceptor');
//});
//
//app.directive("modalShow", function ($parse) {
//  return {
//    restrict: "A",
//    link: function (scope, element, attrs) {
//
//      //Hide or show the modal
//      scope.showModal = function (visible, elem) {
//        if (!elem)
//          elem = element;
//
//        if (visible)
//          $(elem).modal("show");                     
//        else
//          $(elem).modal("hide");
//      };
//
//      //Watch for changes to the modal-visible attribute
//      scope.$watch(attrs.modalShow, function (newValue, oldValue) {
//        scope.showModal(newValue, attrs.$$element);
//      });
//
//      //Update the visible value when the dialog is closed through UI actions (Ok, cancel, etc.)
//      $(element).bind("hide.bs.modal", function () {
//        $parse(attrs.modalShow).assign(scope, false);
//        if (!scope.$$phase && !scope.$root.$$phase)
//          scope.$apply();
//      });
//      }
//
//  };
//});
