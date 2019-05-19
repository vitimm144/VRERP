angular.module('frontendApp')
  .controller('EmployeeCtrl', function (
  $rootScope,
  $scope,
  $state,
  $http,
  $transitions,
  AuthService,
  gridService,
  AUTH_TOKEN_PATH,
  AUTH_LOGOUT_PATH
) {
  var employee_ctrl = this;
  var url = '/api/employees';
  employee_ctrl.gridOptions = {};
  console.log('employees_ctrl');
  var update_grid = function(){
    var result = gridService.update_grid(url)
    result.then(
      function(response){
        employee_ctrl.employees = response.data.results;
        console.log(employee_ctrl.employees);
      }, function(){
        console.log('erro ao pegar employees');
      });
  }; 
    
  update_grid();
  
  employee_ctrl.edit = function(id){
    $state.go('employees.edit', {"employeeId":id}, { reload: true });
  };
  
  employee_ctrl.excluir = function(url){
   gridService.delete_data(url).then(
    function(){
      $state.transitionTo($state.current, {}, { reload: true });
    }, function(){
      console.log('erro ao pegar employees');
    }); 
  };
    
});

