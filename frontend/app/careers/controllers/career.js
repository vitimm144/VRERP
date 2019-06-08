angular.module('frontendApp')
  .controller('CareerCtrl', function (
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
  var career_ctrl = this;
  var url = '/api/careers';
  career_ctrl.gridOptions = {};
  career_ctrl.dtInstance = {};
  career_ctrl.dtOptions = DTOptionsBuilder.newOptions().withPaginationType(
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
  console.log('careers_ctrl');
  var update_grid = function(){
    var result = gridService.update_grid(url)
    result.then(
      function(response){
        career_ctrl.careers = response.data.results;
        console.log(career_ctrl.careers);
      }, function(){
        console.log('erro ao pegar careers');
      });
  };
    
  update_grid();
  career_ctrl.edit = function(id){
    $state.go('careers.edit', {"careerId":id}, {reload:true});
  };
  
  career_ctrl.excluir = function(url){
   gridService.delete_data(url).then(
    function(){
      $state.transitionTo($state.current, {}, { reload: true });
    }, function(){
      console.log('erro ao pegar careers');
    }); 
  };
    
});

