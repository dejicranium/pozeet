	<template id='sidebar-template' >
		<div class="sidebar" v-show='show_sidebar' @click="closeModal"> 
			<div class="sidebar-container" @click.stop>
				
				<div class='profile-info'>
					
					<img v-if='user.userPic' 
						:src='user.userPic' 
						class='avatar'
						 @click='window.open("http://localhost:6543/profile/")'/> 
						 			
					<span @click="openProfile">View Profile</span>
		
					<div class='following-details'>
						<p>{{user.num_of_followers}} followers</p> 
						<p>{{user.num_of_followed}} followed</p> 

					</div>
				</div>

				<div class="sidebar-content">
					
					<p onclick='window.open("http://localhost:6543/logout", "_self")'>Logout</p>
					<p onclick='window.open("http://localhost:6543/trending")'>Trending</p>

					
					<p @click='openPollsVotedIn'>Polls Voted In </p>
					<p @click="openOpinionsVotedIn">Opinions Voted In</p>
					
					<p @click='showSubscriptions = !showSubscriptions' :class="[showSubscriptions? sidebarContentSelectedClass : '']">My Subscriptions </p>
						<li v-if='showSubscriptions' v-for='subscription in sortedSubscriptionsList'  @click='goToCategoryPage(subscription.categoryId)'>{{subscription.categoryName}} <i class="fas fa-minus" @click='goToCategoryPage(subscription.categoryId)'></i></li>
					
					<p @click='showCategories = !showCategories' :class="[showCategories? sidebarContentSelectedClass : '']">Other Categories</p>
						<li v-if='showCategories' v-for='category in categories' @click='goToCategoryPage(category.categoryId)'>{{category.categoryName}}</li>
					
				</div>

			</div>
		</div>
	</template>


<script>
	var siteUrl = 'http://localhost:6543';
	import axios from 'axios';
	var userId = document.getElementById("user-id-signifier").innerText;
	var userSlug = document.getElementById("user-slug-signifier").innerText;

	export default { 
		props: ['close_modal', 'categories', 'show_sidebar', 'user'],

		data(){
			return{
				subscriptions: [],
				sidebarContentSelectedClass: 'sidebar-content-selected',
				showSubscriptions: false,
				showCategories: false,
			}
		},

		computed:{
			sortedSubscriptionsList(){
				var sortedSubscriptions = this._sortCategoryList(this.subscriptions);
				return sortedSubscriptions;
			},

		},

		methods: {

			closeModal(){
				this.$emit('close_modal', false);

			},
			openOpinionsVotedIn(){
				window.open(siteUrl +  '/opinions_voted_in', "_self");
			},

			goToCategoryPage(categoryId){
				window.open(siteUrl + '/polls/category_id=' + categoryId);
			},
			unsubscribeFromCategory(categoryId){
				var category = this.subscriptions.filter(c=> c.categoryId==categoryId);
				var category = category[0]; //because the above returns a list of one object;
				var categoryIndex = this.subscriptions.indexOf(category); //we need the index of the category so we can remove it from list of categories

				this.subscriptions.splice(categoryIndex, 1);
				this.categories.push(category);
			},

			showSubscriptions(){
				this.$emit('act_show_subscriptions', true);
			
			},
			_sortCategoryList(list){
				list.sort(function(a, b){
					if (a.categoryName < b.categoryName) return -1;
					if (a.categoryName > b.categoryName) return 1;
				})
				return list;
			},

			openProfile: function(){
				window.open(siteUrl + '/profile/' + userId + '/' + userSlug, '_self');
			},

			openPollsVotedIn: function(){
				window.open(siteUrl + '/polls_voted_in/', '_self');

			},

		},

		created(){
			axios.get(siteUrl + '/show_subscriptions').then(response => {
				this.subscriptions = response.data.subscriptions;
			});
		}
	}

</script>