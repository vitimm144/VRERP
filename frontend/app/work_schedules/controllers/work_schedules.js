angular.module('frontendApp')
  .controller('WorkScheduleCtrl', function (
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
  var work_schedule_ctrl = this;
  var url = '/api/work_schedules';
  work_schedule_ctrl.gridOptions = {};
  work_schedule_ctrl.dtInstance = {};
  work_schedule_ctrl.dtOptions = DTOptionsBuilder.newOptions().withPaginationType(
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
  work_schedule_ctrl.employees = {};
  console.log('work_schedules_ctrl');
  var update_grid = function(){
    var result = gridService.update_grid(url)
    result.then(
      function(response){
        work_schedule_ctrl.work_schedules = response.data.results;
        console.log(work_schedule_ctrl.work_schedules);
      }, function(){
        console.log('erro ao pegar work_schedules');
      });
  }; 
  $http.get('/api/employees').then(function(data){
    console.log(data);
    angular.forEach(data.data.results, function(result){
      work_schedule_ctrl.employees[result.id] = result.name
    });
            console.log(work_schedule_ctrl.employees);
    
  });
  work_schedule_ctrl.behavior_types = {
    "A": 'Advertência',
    "P": 'Prêmio'
  }
    
  update_grid();
  work_schedule_ctrl.edit = function(id){
    $state.go('work_schedules.edit', {"workScheduleId": id}, { reload: true })
  };
  work_schedule_ctrl.excluir = function(url){
   gridService.delete_data(url).then(
    function(){
      $state.transitionTo($state.current, {}, { reload: true });
    }, function(){
      console.log('erro ao pegar work_schedules');
    }); 
  };
    
});

