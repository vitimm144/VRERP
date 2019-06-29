angular.module('frontendApp')
  .controller('BehaviorSheetCtrl', function (
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
  var behavior_sheet_ctrl = this;
  var url = '/api/behavior_sheets';
  behavior_sheet_ctrl.gridOptions = {};
  behavior_sheet_ctrl.dtInstance = {};
  behavior_sheet_ctrl.dtOptions = DTOptionsBuilder.newOptions().withPaginationType(
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
  console.log('behavior_sheets_ctrl');
  var update_grid = function(){
    var result = gridService.update_grid(url)
    result.then(
      function(response){
        behavior_sheet_ctrl.behavior_sheets = response.data.results;
        console.log(behavior_sheet_ctrl.behavior_sheets);
      }, function(){
        console.log('erro ao pegar behavior_sheets');
      });
  };
  behavior_sheet_ctrl.behavior_types = {
    "A": "Advertência",
    "P": "Prêmio",
    "AT": "Atestado",
    "F": "Falta"
  };
    
  update_grid();
  behavior_sheet_ctrl.edit = function(id){
    $state.go('behavior_sheets.edit', {"behaviorSheetId": id})
  };
  behavior_sheet_ctrl.excluir = function(url){
   gridService.delete_data(url).then(
    function(){
      $state.transitionTo($state.current, {}, { reload: true });
    }, function(){
      console.log('erro ao pegar behavior_sheets');
    }); 
  };
    
});

