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
  AUTH_LOGOUT_PATH,
  DTOptionsBuilder,
  DTColumnDefBuilder
) {
  var employee_ctrl = this;
  var url = '/api/employees';
  employee_ctrl.gridOptions = {};
  employee_ctrl.dtInstance = {};
  employee_ctrl.dtOptions = DTOptionsBuilder.newOptions().withPaginationType(
    'full_numbers'
  ).withDisplayLength( 20 ).withLanguage(
    {
      "sEmptyTable": "Nenhum registro encontrado",
      "sInfo": "Mostrando de _START_ até _END_ de _TOTAL_ registros",
      "sInfoEmpty": "Mostrando 0 até 0 de 0 registros",
      "sInfoFiltered": "(Filtrados de _MAX_ registros)",
      "sInfoPostFix": "",
      "sInfoThousands": ".",
      "sLengthMenu": "_MENU_ resultados por página",
      "sLoadingRecords": "Carregando...",
      "sProcessing": "Processando...",
      "sZeroRecords": "Nenhum registro encontrado",
      "sSearch": "Pesquisar",
      "oPaginate": {
          "sNext": "Próximo",
          "sPrevious": "Anterior",
          "sFirst": "Primeiro",
          "sLast": "Último"
      },
      "oAria": {
          "sSortAscending": ": Ordenar colunas de forma ascendente",
          "sSortDescending": ": Ordenar colunas de forma descendente"
      }
    }
  ).withOption( 'scrollY', '75vh' ).withOption(
    'scrollCollapse',
    true
  ).withOption( 'paging', true );
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
  
  $http.get('/api/careers').then(function(data){
    employee_ctrl.careers = {};
    angular.forEach(data.data.results, function(career){
      employee_ctrl.careers[career.id] = career.title;
    });
    console.log(employee_ctrl.careers);
    
  });
  
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

