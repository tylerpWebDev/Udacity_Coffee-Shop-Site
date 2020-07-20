/* @TODO replace with your variables
 * ensure all variables on this page match your project
 * export const environment = {
 *  production: false,
 *  apiServerUrl: 'http://127.0.0.1:5000/', // the running FLASK api server url
 *  auth0: {
 *    url: 'https://typcoffeeshop.us.auth0.com/', // the auth0 domain prefix
 *    audience: 'coffeeshop', // the audience set for the auth0 app
 *    clientId: '1dvl0GVfWwQP2syaydUyCpI3uvybH1s7', // the client id generated for the auth0 app
 *    callbackURL: 'https://localhost:8100/', // the base url of the running ionic application. 
 *  }
 *};
*/

export const environment = {
  production: false,
  apiServerUrl: '127.0.0.1:5000',
  auth0: {
    url: 'typcoffeeshop.us',
    audience: 'coffeeshop',
    clientId: '1dvl0GVfWwQP2syaydUyCpI3uvybH1s7',
    callbackURL: 'https://localhost:8100'
  }
};


