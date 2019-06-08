angular.module('frontendApp')
  .controller('WorkShiftCtrl', function (
  $rootScope,
  $scope,
  $state,
  $http,
  $transitions,
  $stateParams,
  AuthService,
  gridService,
  AUTH_TOKEN_PATH,
  AUTH_LOGOUT_PATH,
  DTOptionsBuilder,
  DTColumnDefBuilder
) {
  
  var work_shift_ctrl = this;
  
  var url = '/api/work_shifts';
  work_shift_ctrl.work_schedule_id = $stateParams.workScheduleId;
  var filtered_url = '/api/work_shifts/?work_schedule=' + work_shift_ctrl.work_schedule_id;
  work_shift_ctrl.gridOptions = {};
  work_shift_ctrl.dtInstance = {};
  work_shift_ctrl.dtOptions = DTOptionsBuilder.newOptions().withPaginationType(
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
  work_shift_ctrl.employees = {};
  console.log('work_shifts_ctrl');
  var update_grid = function(){
    var result = gridService.update_grid(filtered_url)
    result.then(
      function(response){
        work_shift_ctrl.work_shifts = response.data.results;
        console.log(work_shift_ctrl.work_shifts);
      }, function(){
        console.log('erro ao pegar work_shifts');
      });
  } 
  $http.get('/api/employees').then(function(data){
    console.log(data);
    angular.forEach(data.data.results, function(result){
      work_shift_ctrl.employees[result.id] = result.name
    });
    console.log(work_shift_ctrl.employees);
    
  });
  work_shift_ctrl.behavior_types = {
    "A": 'Advertência',
    "P": 'Prêmio'
  }
    
  update_grid();
  work_shift_ctrl.edit = function(id){
    $state.go(
      'work_schedules.work_shift_edit',
       {
         "workShiftId": id,
         "workScheduleId": work_shift_ctrl.work_schedule_id
       }
    )
  }
  work_shift_ctrl.excluir = function(url){
   gridService.delete_data().then(
    function(){
      update_grid();
    }, function(){
      console.log('erro ao pegar work_shifts');
    }); 
  }
  $transitions.onSuccess({}, function() {
    console.log('Transition on success');
    update_grid();
    
  });
    
});

