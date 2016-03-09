module.exports={
	entry :{
	    home : "./app/components/Home.js",
	    auth : "./app/components/Auth.js"
	},
	output :{
		filename: "../Offline-entertainer/org/ensae/offline_entertainer/server/public/[name].bundle.js"
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