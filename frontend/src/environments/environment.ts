/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'udacity-fsnd-coffee-shop.us', // the auth0 domain prefix https://udacity-fsnd-coffee-shop.us.auth0.com/api/v2/
    audience: 'drinks', // the audience set for the auth0 app
    clientId: 'YOAi6W01Kb3TFhLBA7S5mZt1u2iy9N73', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
