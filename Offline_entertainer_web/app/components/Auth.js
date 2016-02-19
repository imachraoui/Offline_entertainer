var React = require('react');
var ReactDOM = require('react-dom');
var marked = require('marked');


var ArticleBox = React.createClass({
   getInitialState: function() {
    return {data: []};
  },
  loadCommentsFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'text',
      cache: false,
      success: function(data) {
        window.location.replace(data);
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url_reload, status, err.toString());
      }.bind(this)
    });
  },
  componentDidMount : function(){
    this.loadCommentsFromServer();
    //setInterval(this.loadCommentsFromServer, this.props.pollInterval);
  },
  render: function() {
    return (
     <div className="ArticleBox">
        Vérification des droits ...
      </div>
    );
  }
});

ReactDOM.render(
  <ArticleBox url="http://127.0.0.1:3000/api/auth" pollInterval={2000}/>,
  document.getElementById('content')
);