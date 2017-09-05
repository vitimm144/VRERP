angular.module('frontendApp')
  .controller('EmployeeEditCtrl', function (
//  $rootScope,
  $scope,
  $stateParams,
  $state,
  Upload,
  $http,
  AuthService,
  formService,
  alertService,
  AUTH_TOKEN_PATH,
  AUTH_LOGOUT_PATH
){
  var employee_edit_ctrl = this;
  employee_edit_ctrl.base_url = 'api/employees/';
  employee_edit_ctrl.url = 'api/employees/';
  employee_edit_ctrl.file = null;
  employee_edit_ctrl.careers = [];
  console.log('stateParams');
  console.log($stateParams);
  
  $http.get('/api/careers').then(function(data){
    console.log(data);
    employee_edit_ctrl.careers = data.data.results;
  });
  
  
  if ($stateParams.employeeId){
    employee_edit_ctrl.url += $stateParams.employeeId + '/';
    console.log('employee id ', $stateParams.employeeId);
    employee_edit_ctrl.method = 'PUT';
    $http.get(employee_edit_ctrl.url).then(function(data){
      console.log(data);
      data.data.salary = data.data.salary.replace('.', ',');
      employee_edit_ctrl.employee = data.data;
//      employee_edit_ctrl.employee.salary.replace('.', ',');
    });
  }else{
    employee_edit_ctrl.method = 'POST';
    employee_edit_ctrl.employee = {};
  }
  
  employee_edit_ctrl.submit = function(file) {
            console.log(file);
    if(typeof employee_edit_ctrl.employee.salary === "string"){
      employee_edit_ctrl.employee.salary = parseFloat(
        employee_edit_ctrl.employee.salary.replace(',', '.')
      );
    }
    
    if (file){
      file.upload = Upload.upload({
        method : employee_edit_ctrl.method,
        url: employee_edit_ctrl.url,
        data: employee_edit_ctrl.employee,
        file:file,
        fileFormDataName: 'picture' 
      });
      console.log('PUT');

      file.upload.then(function (response) {
        var message = 'Operação realizada com sucesso';
        alertService.message(message, 'success');
        $state.go( '^' );
      }, function (response) {
        if (response.status > 0)
          $scope.errorMsg = response.status + ': ' + response.data;
          var message = 'Erro na operação'
          alertService.message(message, 'danger');
      }, function (evt) {
        // Math.min is to fix IE which reports 200% sometimes
        file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
      });
    } else {
      console.log('PATH');
      console.log(employee_edit_ctrl.url);
      delete(employee_edit_ctrl.employee.picture)
      result = formService.saveFormData(
        employee_edit_ctrl.employee,
        employee_edit_ctrl.base_url
        
      );
      result.then(
        function (response) {
          var message = 'Operação realizada com sucesso';
          alertService.message(message, 'success');
          $state.go( '^' );
        }, 
        function (response) {
          var message = 'Erro na operação'
          alertService.message(message, 'danger');
        }
      );
    }
  };
});



