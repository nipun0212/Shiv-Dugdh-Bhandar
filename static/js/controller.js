'use strict';
var dairyApp = dairyApp || {}

dairyApp.controllers = angular.module('customerControllers',['ui.bootstrap']);

dairyApp.controllers.controller('MainController',function($scope){
	$scope.message = "hello nipun!"
});

dairyApp.controllers.controller('AddCustomer',function($scope,$location){
	$scope.message = "hello nipun!";
	$scope.customer = $scope.customer || {};
	$scope.customer.credit = 0.0;
	$scope.customer.debit = 0.0;
	$scope.init = function () {
                gapi.client.dairymanagement.createCustomer($scope.customer).
                    execute();
                   $location.path('/')
                }
});

dairyApp.controllers.controller('AddItem',function($scope,$location){
	$scope.message = "hello n66ipun!";
	$scope.item = $scope.item || {};
	$scope.init = function () {
      console.log($scope.item);
                gapi.client.dairymanagement.createItem($scope.item).execute();
                $location.path('/')
                }
});

dairyApp.controllers.controller('vieworder',function($scope,$location,$routeParams){

  
  $scope.customer = $scope.customer || {}
  $scope.orders = $scope.orders || {}
  $scope.customer.custId = $routeParams.custId
  gapi.client.dairymanagement.getOrder($scope.customer).execute()
  gapi.client.dairymanagement.getOrder($scope.customer).execute(function (resp) {
      $scope.$apply(function (){
      $scope.orders = resp.orderList;
      });
      
  });

});

dairyApp.controllers.controller('PlaceOrder',function($scope,$location,$filter){
	
$scope.init = function () {
  	

	$scope.item = {itemId:-1}
  $scope.items = $scope.items || {};
	$scope.customers = $scope.customer || {};
	$scope.customers.credit = 0.0;
	$scope.customers.debit = 0.0;
	console.log($scope.message);
	$scope.custLastPurchase = $scope.custLastPurchase || {};
	$scope.itemcust =$scope.itemcust || {}
	
	gapi.client.dairymanagement.getItemList().execute(function (resp) {
               			$scope.$apply(function (){
               				$scope.items = resp.itemList;
               			});
                    });
                                                                                                                
                gapi.client.dairymanagement.getCustomerList().execute(function (resp) {
                    $scope.$apply(function (){
                    $scope.customers = resp.customerList;
                    });
                    
                });
                		
                
};
$scope.getQuantity = function (){
   console.log($scope.item.date);
    $scope.item.date = $filter('date')($scope.item.date,'MM/dd/yy'); 
    console.log($scope.item)
     console.log($scope.item)
gapi.client.dairymanagement.getDateSpecifiedPurchase($scope.item).execute(function (resp) {
               			$scope.$apply(function (){
               				$scope.custLastPurchase = resp.custItemQuantityList;
                      angular.merge($scope.custLastPurchase, $scope.customers);
               			
               			});
               			
                    });
};


$scope.submit = function (){
	$scope.itemcust.itemId = $scope.item.itemId
  console.log($scope.itemcust.orderDate);
  $scope.itemcust.orderDate = $filter('date')($scope.itemcust.orderDate ,'MM/dd/yy:HH:mm:ss'); 
    console.log($scope.itemcust.orderDate);
  console.log($scope.custLastPurchase);
	angular.forEach($scope.custLastPurchase,function(value,index){
                console.log(value.itemQuantity);
                console.log(value.custId);
                $location.path('/'); 
                   $scope.itemcust.custId = value.custId;
                   console.log($scope.itemcust.custId);
                    $scope.itemcust.itemQuantity = value.itemQuantity;
               gapi.client.dairymanagement.placeOrder($scope.itemcust).execute()
            });
};
	
});


dairyApp.controllers.controller('showcustomers',function($scope,$location){
	
$scope.init = function () {
  	

	$scope.item = {itemId:-1}
  	$scope.items = $scope.items || {};
	$scope.customers = $scope.customer || {};
	$scope.customers.credit = 0.0;
	$scope.customers.debit = 0.0;
	console.log($scope.message);
	$scope.custLastPurchase = $scope.custLastPurchase || {};
	$scope.itemcust =$scope.itemcust || {}
	
                gapi.client.dairymanagement.getCustomerList().execute(function (resp) {
                    $scope.$apply(function (){
                    $scope.customers = resp.customerList;
                    });
                    
                });
                		
                
};
$scope.changeLocation = function (custId) {
  $location.path('/customer/vieworder/' + custId).replace();
}

});

