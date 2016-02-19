var React = require('react');
var ReactDOM = require('react-dom');
var marked = require('marked');

var Comment = React.createClass({
  rawMarkup: function() {
    var rawMarkup = marked(this.props.children.toString(), {sanitize: true});
    return { __html: rawMarkup };
  },
  render: function() {
    return (
      <div className="comment">
        <h2 className="commentAuthor">
          {this.props.author}
        </h2>
        {marked(this.props.children.toString())}
		<span dangerouslySetInnerHTML={this.rawMarkup()}/>
      </div>
    );
  }
});

var CommentForm = React.createClass({
  getInitialState : function(){
    return {author: '', text: ''};
  },
  handleAuthorChange: function(e) {
    this.setState({author: e.target.value});
  },
  handleTextChange: function(e) {
    this.setState({text: e.target.value});
  },
  handleSubmit: function(e) {
    e.preventDefault();
    var author = this.state.author.trim();
    var text = this.state.text.trim();
    if (!text || !author) {
      return;
    }
    // TODO: send request to the server
    this.props.onCommentSubmit({author: author, text: text});
    this.setState({author: '', text: ''});
  },
  render: function() {
    return (
     <form className="commentForm" onSubmit={this.handleSubmit}>
        <input type="text" placeholder = "Your name" value={this.state.author} onChange={this.handleAuthorChange}/><br/>
        <input type="text" placeholder = "Your comment" value={this.state.text} onChange={this.handleTextChange}/><br/>
        <input type="submit" value="Post" />
     </form>
    );
  }
});

var CommentList = React.createClass({
  render: function(){
	  var commentNodes = this.props.data.map(function(comment) {
		  return (
			<Comment author={comment.author} key={comment.id}>
			  {comment.text}
			</Comment>
		  );
	  });
	return (
      <div className="commentList">
        {commentNodes}
      </div>);
  }
});

var CommentBox = React.createClass({
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
   handleCommentSubmit: function(comment) {
     $.ajax({
      url: this.props.url,
      dataType: 'json',
      type: 'POST',
      data: comment,
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  componentDidMount : function(){
    this.loadCommentsFromServer();
    //setInterval(this.loadCommentsFromServer, this.props.pollInterval);
  },
  render: function() {
    return (
     <div class="CommentBox">
        Hello world! I am a CommentBox.
		<CommentForm onCommentSubmit={this.handleCommentSubmit} />
		<CommentList data={this.state.data}/>
      </div>
    );
  }
});

ReactDOM.render(
  <CommentBox url_reload="http://127.0.0.1:3000/api/articles" pollInterval={2000} url="http://127.0.0.1:3000/api/addArticle"/>,
  document.getElementById('content')
);