var React = require('react');
var ReactDOM = require('react-dom');
var marked = require('marked');
var bootstrap = require('react-bootstrap');

var Panel = ReactBootstrap.Panel;
var ArticleForm = React.createClass({
   getInitialState : function(){
    return {url: ''};
  },
   handleURLChange: function(e) {

    this.setState({url: e.target.value});
  },
  handleSubmit: function(e) {
    e.preventDefault();

    if (!this.state.url) {
      return;
    }
    this.props.onArticleSubmit({url:this.state.url,user_id:this.props.userid});
  },
  render: function() {
    return (
     <form className="articleForm" onSubmit={this.handleSubmit}>
        <input type="text" placeholder = "Your URL" value={this.state.url} onChange={this.handleURLChange}/><br/>
        <input type="submit" value="Post" />
     </form>
    );
  }
});

var Article = React.createClass({
  render: function() {
    return (
     <div className="Article" >
        <Panel header={this.props.title} bsStyle="primary">
            {this.props.children.toString()}
        </Panel>
      </div>
    );
  }
});

var ArticleList = React.createClass({
   render: function(){
	  var articles = this.props.data.map(function(article) {
		  return (

			<Article text={article.text} title={article.title} key={article.url}>
			  {article.text}
			</Article>
		  );
	  });
	return (
      <div className="ArticleList">
        {articles}
      </div>);
  }
});

var ArticleBox = React.createClass({
   getInitialState: function() {
    return {data: []};
  },
  loadCommentsFromServer: function() {
    $.ajax({
      url: this.props.url_reload,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url_reload, status, err.toString());
      }.bind(this)
    });
  },
  handleSubmit : function(url){
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      type: 'POST',
      data: url,
      success: function(data) {
        this.setState({data: data});
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
        Ajouter un article
        <ArticleForm onArticleSubmit={this.handleSubmit} userid="1"/>
        La liste d articles :
		<ArticleList data={this.state.data}/>
      </div>
    );
  }
});

ReactDOM.render(
  <ArticleBox url_reload="http://127.0.0.1:3000/api/articles/1" pollInterval={2000} url="http://127.0.0.1:3000/api/addArticle" />,
  document.getElementById('content')
);