var React = require('react');
var ReactDOM = require('react-dom');
var marked = require('marked');
var bootstrap = require('react-bootstrap');
var Slider = require('react-slick');

var Panel = ReactBootstrap.Panel;
var user_id = window.location.search.split("=")[1];


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
        <input type="text" placeholder = "Votre URL" value={this.state.url} onChange={this.handleURLChange}/><br/>
        <input type="submit" value="Post" />
     </form>
    );
  }
});

var Article = React.createClass({
  getStyle : function(){
   var style;
    if(this.props.isArticle != 1){
        style="danger";
    }else{
        style = "primary"
    }
    return(style);
  },
  render: function() {
    return (
     <div className="Article" >
        <Panel header={this.props.title} bsStyle={this.getStyle()}>
            {this.props.children.toString()}
        </Panel>
      </div>
    );
  }
});

var ArticleList = React.createClass({
   getInitialState: function() {
    return {data: []};
  },
  shouldComponentUpdate: function() {
    return true;
  },
  update : function(){
    this.state.data.push(this.props.data);
  },
   render: function(){
       //this.update();
       var test = this.props.data;
       test.sort(function(a, b) {return b.time_added - a.time_added})
	  var articles = test.map(function(article) {
		  return (
			<Article text={article.text} title={article.title} key={article.url} isArticle={article.is_article}>
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
      url: this.props.url_reload + user_id,
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
        this.state.data.push(data[0])
        data = this.state.data
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url_reload, status, err.toString());
      }.bind(this)
    });
  },
  componentDidMount : function(){
    this.loadCommentsFromServer();
  },
  render: function() {
    return (
     <div className="ArticleBox">
        Ajouter un article
        <ArticleForm onArticleSubmit={this.handleSubmit} userid={user_id}/>
        La liste d articles :
		<ArticleList data={this.state.data}/>
      </div>
    );


  }
});

ReactDOM.render(
  <ArticleBox url_reload="http://127.0.0.1:3000/api/articles/" pollInterval={2000} url="http://127.0.0.1:3000/api/addArticle" />,
  document.getElementById('content')
);

