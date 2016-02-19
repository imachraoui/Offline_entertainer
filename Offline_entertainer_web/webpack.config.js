module.exports={
	entry :{
	    test : "./app/components/Main.js",
	    home : "./app/components/Home.js",
	    auth : "./app/components/Auth.js"
	},
	output :{
		filename: "public/[name].bundle.js"
	},
	module : {
		loaders : [
		{
			 // "test" is commonly used to match the file extension
			test: /\.jsx?$/,

			// "include" is commonly used to match the directories
			exclude: /(node_modules|bower_components)/,

			// "exclude" should be used to exclude exceptions
			// try to prefer "include" when possible

			// the "loader"
			loader: "babel",
			query : {
				presets : ['react','es2015']
			}
		}
		]
	}

}