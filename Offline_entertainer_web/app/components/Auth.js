var React = require('react');
var ReactDOM = require('react-dom');

var SelectUser = React.createClass({
   getInitialState : function(){
    return {user: ''};
  },
  getUsers: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(data) {
         var users = document.getElementById('user');
         for(var index in data){
            users.options[users.options.length] = new Option(data[index], data[index]);
         }
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  redirectToArticles: function() {
    $.ajax({
      url: this.props.url_auth,
      dataType: 'text',
      cache: false,
      success: function(data) {
        window.location.replace(data+this.state.user);
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
   handleUserChange: function(e) {
    e.preventDefault();
    this.setState({user: e.target.value});
  },
  handleSubmit: function(e) {
    e.preventDefault();

    if (!this.state.user) {
      return;
    }
    this.redirectToArticles();
  },
  componentDidMount : function(){
    this.getUsers();
  },
  render: function() {

    return (

    <form className="navbar-form"  onSubmit={this.handleSubmit}>

        Sélectionner un id d'utilisateur : <select id="user" placeholder="User ID" value={this.state.user} onChange={this.handleUserChange} className="span2"/><br/>
        <p></p>
        <input type="submit" className="btn btn-primary btn-xl page-scroll" value="Envoyer" />
     </form>

    );
  }
});

ReactDOM.render(
  <SelectUser url="http://127.0.0.1:3000/api/users" url_auth="http://127.0.0.1:3000/api/auth"/>,
  document.getElementById('content')
);