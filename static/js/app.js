'use strict';

/**
 * @ngdoc object
 * @name conferenceApp
 * @requires $routeProvider
 * @requires conferenceControllers
 * @requires ui.bootstrap
 *
 * @description
 * Root app, which routes and specifies the partial html and controller depending on the url requested.
 *
 */
var app = angular.module('dairyApp',
    ['customerControllers', 'ngRoute', 'ui.bootstrap']).
    config(['$routeProvider',
    function($routeProvider){
	$routeProvider.when('/customer/addcustomer',{
		 templateUrl : '/partials/addcustomer.html',
		controller : 'AddCustomer'
	}).when('/customer/additem',{ 
		templateUrl :'/partials/additem.html',
		controller : 'AddItem'
	}).when('/customer/placeOrder',{ 
		templateUrl :'/partials/addorder.html',
		controller : 'PlaceOrder'

	}).when('/customer/showcustomers',{ 
		templateUrl :'/partials/showcustomers.html',
		controller : 'showcustomers'

	}).when('/customer/vieworder/:custId',{ 
		templateUrl :'/partials/vieworder.html',
		controller : 'vieworder'

	}).
                otherwise({
                    redirectTo: 'UserInterface/index.html'
                });
}]);

