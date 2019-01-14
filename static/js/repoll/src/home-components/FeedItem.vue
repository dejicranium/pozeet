<template id='feed-item'>
        <div class="feed-container">
				<!--you will have to re-write the styles. This modal imports from authentication modal-->

			<!--This div will be shown for poll activities --> 
            <div class="feed-card" v-if="activity.type=='poll'" tabindex='0'>
                
				<div class='poll'>

					<div class='trigger' v-if='activity.trigger' style='margin-bottom: 5px; padding:10px; padding-left:25px;'>
						<p style='color:darkgrey; font-size:11px;'>{{activity.triggerActor}}  {{activity.trigger}}</p>

					</div>

					<div class="avatar">
                	     <img v-if='activity.userPic == null' src="https://www.w3schools.com/howto/img_avatar.png"/> 
						 <img v-if='activity.userPic != null' :src='activity.userPic'>
                	</div>


                	<div class="beside-avatar-box">
                    	<div class="author-details">
                        	<p class="name" @click="openUserProfile">{{activity.userName}}</p>
                        	<p class="username"></p>
							<p class='time-added'>{{activity.timeAdded}}</p>

							<!--<i v-if='!userJustFollowed' class="fas fa-user-plus"></i>
							<p @click='followOrUnfollowUser' style='position:absolute; right: 0; margin-right:18px; color: teal;' v-if='!userIsFollowing'>Follow</p>
							-->
					
						</div>

	                    <div class="categories-container">

	                    </div>

	                    <h6 class="poll-question"><a :href="'localhost:6543/poll/' + activity.id + '/'">{{activity.question}}</a></h6>
                    
					
						<div class="poll-info">
							<div v-if='infoHasLink != undefined && infoHasLink == null' class='link-info' style='display:flex; padding: 5px;; flex-direction:row; border:0.5px solid lightgrey; border-radius:10px;'>
								<img :src='infoLinkThumb' width='150' height='100' style='margin-right:5px;'/>
								<div style='display:flex; flex-direction:column'>
									<h4>{{infoLinkTitle}}</h4>
									<p>{{infoLinkDescription}}</p>
								</div>
							</div>
						
							<div v-if='activity.info' style='margin-bottom:3px; white-space:;'>
								{{activity.info}}
							</div>

							<div v-if='activity.imageInfo'>
								<img :src='activity.imageInfo' style=' max-width: 100%; max-height:300px; border-radius:10px'>
							</div>
						</div>
					


						<!--if the poll has ended, just show the results already! --> 
						<template v-if='!pollHasEnded'>						
							<!-- this is the default. Shows when the user has not voted -->
							<template v-if='!isPicturePoll'>
								<template v-if='!userHasVoted && !seenPollResults'>
									<div class='options' v-for='option in activity.options' :option='option' :key="option.id + activity.id">
										<label>
											<input type="radio" @click='optionChosen(option.id)' name='option' :value='option.id'>
											<span class='checkmark'></span>
											{{option.option}}
										</label>

									</div>
								</template>
								<!-- once the user has voted, this template will come up! --> 
								<!--<template v-else-if='userHasVoted && !isPicturePoll'>
								--> 
								<template v-else-if="userHasVoted || seenPollResults">
									<div class='options'>
	 									<div class="ans-cnt" v-for="option in calculatedScores" :option='option' :key="option.id + activity.id">
											<div class="ans">
                    	            			<div class="ans-voted">
                        	            			<span class="percent">{{option.percent}}</span>
                            	        			<span class="txt">{{option.option}}</span>
                                				</div>
                                				<span class="first-bg"></span>
                                				<span :class="{bg:true}" :style='{width: option.percent}'></span>
    	                        			</div>
										</div>
            	        			</div>
								</template>

							</template>	

							<template v-else>
								 <template v-if='!userHasVoted && !seenPollResults'>
					   				<div class='picture-options'>
										<label v-for='option in activity.options' :option="option">
											<input type='radio' @click='optionChosen(option.id)' name='option' :value='option.id'/>
											<img :src='option.image'/>

											<span class='checkbox'></span>

											<span>{{option.option}}</span>
							 			</label>
					   				</div>
								</template>

								<template v-else-if='userHasVoted || seenPollResults'>
					   				<div class='picture-options'>
										<label v-for='option in calculatedScores' :option="option">
											<input type='radio'  @click='optionChosen(option.id)' name='option' :value='option.id'/>
											<img :src='option.image'/>

											<!--<span class='checkbox' style='opacity:0'></span>-->
											<label style='background-color: rgba(0, 0, 0, .1);' :style='{width:option.percent}'>
											<span style='color:black;font-weight:bold;'>{{option.percent}}</span>
											</label>
							 			</label>

					   				</div>

								</template>
							</template>
					
						</template>

						<template v-else>
							<template v-if='!isPicturePoll'>
								<div class='options'>
	 								<div class="ans-cnt" v-for="option in calculatedScores" :option='option'>
										<div class="ans">
                                			<div class="ans-voted">
                                    			<span class="percent">{{option.percent}}</span>
                                    			<span class="txt">{{option.option}}</span>
                                			</div>
                                			<span class="first-bg"></span>
                                			<span :class="{bg:true}" :style='{width: option.percent}'></span>
                            			</div>
									</div>
                    			</div>
							</template>


							<template v-else>
				   				<div class='picture-options'>
									<label v-for='option in calculatedScores' :option="option">
										<input type='radio' @click='optionChosen(option.id)' name='option' :value='option.id'/>
										<img :src='option.image'/>
							
										<!--<span class='checkbox' style='opacity:0'></span>-->
										<label style='background-color: rgba(0, 0, 0, .1);' :style='{width:option.percent}'>
										<span style='color:black;font-weight:bold;'>{{option.percent}}</span>
										</label>
						 			</label>

				   				</div>

							</template>
						</template> 

						<div style='display:flex; flex-direction="row"'>
                    		<p class="votes">{{totalVotes}} votes </p>
                    		<p class="votes" style="color:darkgrey;cursor:pointer;"> {{activity.timeRemaining}}</p>
					
						</div>
					
						<button v-on:click="vote" v-show='!userHasVoted && !seenPollResults' id='vote-btn'><i class="far fa-check-circle button-icon"></i>Vote</button>
                    	<button v-on:click='addComment' v-show='!userHasVoted && !seenPollResults' id='comment-btn'><i class="far fa-comment button-icon"></i>Comment</button>
                    	<button v-on:click='seeResults' v-show='!userHasVoted && !seenPollResults'><i class="far fa-chart-bar button-icon"></i>Results</button>
						<button v-on:click='share'>Share</button>
						<!--	<button v-on:click='like' v-if='(userHasVoted || seenPollResults) && !activityIsAlreadyLiked'><i class="far fa-thumbs-up button-icon"></i>Like <span>((numOfLikes))</button> -->					
						<button  @click='openBreakDownWindow' v-show='userHasVoted || seenPollResults'><i class="fas fa-chart-pie button-icon"></i>View Breakdown</button>
						<!--	<p style='font-weight:bold; font-size:12px;' v-if='activityIsAlreadyLiked'> {{numOfLikes}} likes</p> -->

					</div>
		
					<div v-show='activity.numOfComments != 0' style='margin-top:5px; padding:5px; text-align:center;vertical-align:middle; border-top:whitesmoke 0.6px solid;'>

						<span style='color:darkgrey'  @click='viewComments'>View Comments</span>

					</div>
				</div>
			</div>
			

		<!---This is the comment div --> 
			<div class="feed-card" v-else-if='activity.type=="comment"' tabindex='0'>
				<div class='trigger' v-if='activity.trigger' style='margin-bottom: 5px; padding:10px; padding-left:20px; border-bottom: solid 0.3px lightgrey;'>
					<p style='color:darkgrey; font-size:11px;'>{{activity.triggerActor}}  {{activity.trigger}}</p>

				</div>
				<div class="avatar">
                     <img v-if='!activity.userPic' src="https://www.w3schools.com/howto/img_avatar.png"/>
					 <img v-else :src='activity.userPic'>
                </div>

                <div class="beside-avatar-box">
                    <div class="author-details">
                        <p class="name" style='font-weight:bold;' @click="openUserProfile">{{activity.commenter}}</p>
                        <p class="username"></p>
                        <p class="action"></p>
                    </div>


                    <h2 class="chosen-option" style="font-weight:bold;">{{activity.option_chosen}}</h2>
                    <p class="comment" style='white-space:;'>{{activity.comment}}</p>


                    <div>
                        <div class="comment-question" v-if='activity.poll' tab-index="0" @click="openPoll">
                            <p class='author-name' style='font-weight:normal; color:teal;'>Poll</p>
                            <p class='author-name' style='font-size:bold;'>{{activity.poll.userName}} <span style="color:lightgray; font-weight:normal;">{{activity.timeAdded}}</span></p>
							<p class='question'>{{activity.poll.question}}</p>
                        </div>
                            
						<div class="comment-question" v-else-if='activity.opinion' tab-index="0" @click="openOpinion">
                            <p class='author-name' style='font-weight:normal; color:teal;'>Opinion</p>
                            <p class='author-name' style='font-size:bold;'>{{activity.opinion.userName}} <span style="color:lightgray; font-weight:normal;">{{activity.opinion.timeAdded}}</span></p>
							<p class='question'>{{activity.opinion.opinion}}</p>

                        </div>

                    </div>

					<button @click='reply'> <i class="fas fa-reply button-icon"></i>Reply </button>
						<!--<button @click='like' :id="[activityIsAlreadyLiked ? 'activityIsAlreadyLikedClass' : '']"><i class="far fa-thumbs-up button-icon"></i>Like</button> -->
						<!--<button @click="share"><i class="far fa-share-square button-icon"></i>Share</button> -->
				</div>
        	</div>



			<div class="feed-card" v-else-if='activity.type=="opinion"' tabindex="0">
				<div class='trigger' v-if='activity.trigger' style='margin-bottom: 5px; padding:10px; padding-left:20px; border-bottom: solid 0.3px lightgrey;'>
					<p style='color:darkgrey; font-size:11px;'>{{activity.triggerActor}}  {{activity.trigger}}</p>

				</div>
				<div class="avatar" v-if='activity.trigger'>
        	        <img v-if='!activity.userPic' src="https://www.w3schools.com/howto/img_avatar.png" style='margin-top:12px;'/>
					<img v-else :src='activity.userPic'>
                </div>

				<div class="avatar" v-else>
                    <img v-if='!activity.userPic' src="https://www.w3schools.com/howto/img_avatar.png"/>
					<img v-else :src='activity.userPic'>
                </div>
				
                <div class="beside-avatar-box">
					<div v-if='activity.trigger' style='margin-bottom:0px;'>
						<p style='color:darkgrey; font-size:11px'>{{activity.triggerActor}} {{activity.trigger}}</p>
					</div>
                        <div class="author-details">
                            <p class="name" style='color;black; font-weight:bold; font-size:12px;' @click="openUserProfile">{{activity.userName}}</p>
                            <p class="username"></p>
							<p class='time-added'>{{activity.timeAdded}}</p>
                        </div>

                        <p class="comment" style='white-space:'>{{activity.opinion}}</p>
						<div style='display:flex; flex-direction:row;'>
							<img id='opinionContextImage' v-for='image in activity.contextImage' :image='image' :src='image.imgLink' style='width:100%; max-height:200px; border-radius:5px;' >

						</div>
						<p class='votes'>{{activity.numOfComments}} reactions</p>



						<button @click='addComment("Agree")' v-if='!activity.userHasVoted'><i class="fa fa-check button-icon" aria-hidden="true"></i>Agree</button>
						<button @click='addComment("Disagree")' v-if='!activity.userHasVoted'><i class="far fa-thumbs-down button-icon"></i>Disagree</button>
						<button v-on:click='share'>Share</button>						
						<button  @click='openBreakDownWindow' v-show='userHasVoted'><i class="fas fa-chart-pie button-icon"></i>View Breakdown</button>

					</div>

            </div>


			<div class="feed-card" v-else-if='activity.type=="reply"' tabindex="0">
				<div class='trigger' v-if='activity.trigger' style='margin-bottom: 5px; padding:10px; padding-left:20px; border-bottom: solid 0.3px lightgrey;'>
					<p style='color:darkgrey; font-size:11px;'>{{activity.triggerActor}}  {{activity.trigger}}</p>

				</div>
					<div class="avatar" v-if='activity.trigger'>
                         <img v-if='!activity.userPic' src="https://www.w3schools.com/howto/img_avatar.png" style='margin-top:12px;'/>
						 <img v-else :src='activity.userPic'>
                    </div>

					<div class="avatar" v-else>
                         <img v-if='!activity.userPic' src="https://www.w3schools.com/howto/img_avatar.png"/>
						 <img v-else :src='activity.userPic'>
                    </div>
				
                    <div class="beside-avatar-box">
						<div v-if='activity.trigger' style='margin-bottom:0px;'>
							<p style='color:darkgrey; font-size:11px'>{{activity.triggerActor}} {{activity.trigger}}</p>
						</div>
                        <div class="author-details">
                            <p class="name" style='color;black; font-weight:bold; font-size:12px;' @click="openUserProfile">{{activity.userName}} <span style='color:teal'>=> {{activity.userRepliedTo}}</span></p>
                            <p class="username"></p>
							<p class='time-added'></p>
                        </div>

                        <p class="comment" style='white-space:'>{{activity.reply}}</p>
						
		                 <div class="comment-question" v-if='activity.comment' tab-index="0" @click="openComment">
                            <p class='author-name' style='font-weight:normal; color:teal;'>Comment</p>
                            <p class='author-name' style='font-size:bold;'>{{activity.comment.commenter}} <span style="color:lightgray; font-weight:normal;">{{activity.comment.timeAdded}}</span></p>
							<p class='question'>{{activity.comment.comment}}</p>


                        </div>						
						<!-- <button><i class="far fa-thumbs-up button-icon" :id="[activityIsAlreadyLiked? 'activityIsAlreadyLikedClass' : '']" @click='like'></i>Like</button> -->
						<button @click='openReply'><i class="fas fa-reply button-icon"></i> Reply </button>

						
	

						
						<p style='text-decoration:; color:darkgrey; margin-top:5px; font-weight: bold; font-size:13px; text-decoration:;' @click='openViewConversationPage'>View conversation</p>
					</div>

            </div>

			<div class="feed-card" v-else-if='activity.type=="demo"' tabindex="0" style='text-align:center;'>
				<div class='trigger' v-if='activity.trigger' style='margin-bottom: 5px; padding:10px; padding-left:20px; border-bottom: solid 0.3px lightgrey;'>
					<p style='color:darkgrey; font-size:11px;'>{{activity.triggerActor}}  {{activity.trigger}}</p>

				</div>
				

                        <div class="author-details">
                            <p class="name" style='color;black; font-weight:bold; font-size:12px;'>{{activity.title}}</p>
                        </div>
						<canvas :id="'metricsChart' + activity.id" style='width:100%' height='400'></canvas>


					

            </div>

    </div>
	

</template>

<script>
	import axios from 'axios';
		var siteUrl = 'http://a78f522e.ngrok.io';
		var chart1 = '';

	export default {
		name: 'FeedItem',
		props: ['activity', 'user_logged_in', 'show_comment_modal', 'show_view_comments_modal'],
		delimiters: ['((', '))'],
		data(){
			return{

				//these are for the polls.
				pollHasEnded: this.activity.hasEnded,
				isPicturePoll: this.activity.isPicturePoll,
				justVotedScore: 0,
				chosenOption: 0,
				chosenOptionName: this.getChosenOptionName(),
				infoHasLink: this.activity.hasUrlInfo,
				infoLinkThumb: this.activity.infoPageThumb,
				infoLinkTitle: this.activity.infoPageTitle,
				infoLinkDescription: this.activity.infoPageDescription,
				userIsFollowing: this.activity.userIsFollowing,
				seenPollResults: this.activity.userHasSeenResults,

				activityUnliked: false,
				activityIsAlreadyLikedClass: 'activityIsAlreadyLikedClass',
			}
			

			
		},
		mounted(){
			if (this.activity.type == 'demo'){
				this.getPollMetrics();
			}
		
		},

		methods:{
			openComment(){
				window.open(siteUrl + '/view_comment/' + this.activity.comment.comment_id, '_self');
			},
			openOpinion(){
				window.open(siteUrl + '/opinion/' + this.activity.opinion.id +'/', '_self');
			},
			openPoll(){
				window.open(siteUrl + '/poll/' + this.activity.opinion.id +'/', '_self');
			},
			openViewConversationPage(){
				window.open(siteUrl + '/view_conversation/conversation_id=' + this.activity.conversationId +'/reply_id=' + this.activity.id, '_self');

			},
			openUserProfile(){
				window.open(siteUrl + '/profile/' + this.activity.userId + "/" + this.activity.userSlug, '_self');
			},

			viewComments(){
				window.open(siteUrl + '/poll/' + this.activity.id +'/', '_self');
			},
			seeVoters(){
				var result = true;
				if (this.user_logged_in == false){
					this.$emit('show_auth_modal', result);
					return 0;
				}

				this.$emit('act_show_voters_modal', '/voters/' + this.activity.id);
				
			},

			reply(){
				var result = true;
				if (this.user_logged_in == false){
					this.$emit('show_auth_modal', result);
					return 0;
				}
				
				this.$emit('set_reply_activity_details', this.activity);
			},

			followUser(){

				var vm = this;
				axios.post(siteUrl + '/follow/' + this.activity.userId, {
				}).then(response =>{
					this.userJustFollowed = true;
					this.userIsFollowing = true;
				});

			},

			unfollowUser(){
				axios.post(siteUrl + "/unfollow/" + this.activity.userId,{
				}).then(response=>{
					this.userJustFollowed = false;
					this.userIsFollowing = false;
				});

			},
	
			followOrUnfollowUser(){
				var result = result;
				if (this.user_logged_in == false){
					this.$emit('show_auth_modal', result);
					return 0;
				}

				if(!this.userJustFollowed){
					this.followUser();
				}
				else{
					this.unfollowUser()
				}


			},

			
			openReply(){

			if (this.user_logged_in == false){
					var result = true;
					this.$emit('show_auth_modal', result);
					return 0;

				}
				this.$emit('act_show_comment_modal', true);
				this.$emit('set_activity_comment_details', this.activity);

				//this will pass the id of the option that was chosen before 
				//the comment button was clicked
				this.$emit('set_option_comment_details',{});
			},

			changeActivityData(id, value){
				this.$set(this.activity. id, value);
			},

			openBreakDownWindow(){
				if (this.user_logged_in == false){
					this.$emit('show_auth_modal', true);
					return 0;
				}

				if (this.activity.type=='opinion'){
					window.open(siteUrl + '/opinion/demographic-metrics/' + this.activity.id, '_self');

				}
				else{
					window.open(siteUrl + '/poll/demographic-metrics/' + this.activity.id, '_self');
				}
			
			},

			
			showViewCommentsModal(){
				this.$emit('act_show_view_comments_modal', true);
			
			},

			closeModal(){
				this.$emit('act_close_comment_modal', false)
			},
			
			like(event){
				var vm = this;
				if (this.user_logged_in == false){
					this.$emit('show_auth_modal', true);
					return 0;
				}
				event.target.disabled = true;

				if (!this.activity.userHasLiked){
					if(this.activity.type == 'reply'){
						vm.activity.numOfLikes += 1;

						axios.post(siteUrl + '/like/', {
							
							reply_id: vm.activity.id,
						}).then(function(response){
							vm.activity.userHasLiked = true;
							event.target.disabled = false;
						}).catch(function(error){
							vm.activity.userHasLiked = false;
							event.target.disabled = false;

						});
					}

					else if(this.activity.type == 'poll'){

						axios.post(siteUrl + '/like/', {
							poll_id: vm.activity.id,

						}).then(function(response){
							vm.activity.userHasLiked = true;
							vm.activity.numOfLikes += 1;
							event.target.disabled = false;


						}).catch(function(error){
							event.target.disabled = false;

						});
					}
					else if (this.activity.type == 'comment'){
						
						event.target.disabled = true;

						axios.post(siteUrl + '/like/', {

						}).then(function(response){
							event.target.disabled = false;

							vm.activity.userHasLiked = true;
							vm.activity.numOfLikes += 1;

						}).catch(function(response){
							event.target.disabled = false;

						});
					}
				}

				else {
					this.unlike(event, this.activity, this.activity.type, this.activity.id);

				}
			},

			unlike(event, activity, activityType, activityId){
				var vm = this; 
				var result = true;
				if (this.user_logged_in == false){
					this.$emit('show_auth_modal', result);
					return 0;
				}

				if (activityType=='poll'){
					
					event.target.disabled = true;

					axios.post(siteUrl + '/unlike/', {
						poll_id: activityId,
					}).then(response=>{
						event.target.disabled = false;

						vm.activity.userHasLiked = false;
						vm.activityUnliked = true;
						vm.activity.numOfLikes -= 1;
					}).catch(function(response){
						vm.activity.userHasLiked = true;
						event.target.disabled = false;

					});

				}

				else if(activityType='opinion'){
					
							event.target.disabled = true;

					axios.post(siteUrl+ '/unlike/', {
						opinion_id: activityId, 
					}).then(response=>{
							event.target.disabled = false;

						vm.activity.userHasLiked = false;
						vm.activity.numOfLikes -= 1;

					}).catch(response=>{
							event.target.disabled = false;

					});

				}

				else if(activityType=='comment'){
							event.target.disabled = true;

					axios.post(siteUrl + '/unlike/' + {
						comment_id: activityId, 
					}).then(response=>{

							event.target.disabled = false;

						vm.activity.userHasLiked = false;
						vm.activity.numOfLikes -= 1;

					}).catch(function(response){
							event.target.disabled = false;

					});
				}
			},
			share(){
				this.$emit('act_show_shareto_modal', true);
				this.$emit('act_set_activity_to_share', this.activity);
			},

			addComment(option){
				var result = true;
				if (this.user_logged_in == false){
					var result = true;
					this.$emit('show_auth_modal', result);
					this.$emit('change_activity_to_refer_to', this.activity);
					return 0;

				}

				if (this.chosenOption  == 0) { //if no option has been chosen
					//check if the activity is an opinion
					if (this.activity.type != 'opinion'){

						alert('Select an option');
						return 0;
					}
				}

				var activities = this.activity.options.filter(i=> i.option == option);
				this.chosenOption = activities[0].id;

				this.$emit('set_activity_comment_details', this.activity);

				//this will pass the id of the option that was chosen before 
				//the comment button was clicked
				this.$emit('set_option_comment_details', this.chosenOption);

				this.$emit('act_show_comment_modal', true);


			},

			optionChosen(optionId){
				this.chosenOption = optionId;

			},

			getChosenOptionName(){
				var chosenOptionId = this.chosenOption;
				for (var i = 0; i < this.activity.options.length; i++){
					if (this.activity.options[i].id == chosenOptionId){
						return this.activity.options.option;
					}
				}
			},

			
			vote(){
				var vm = this;

				if (this.user_logged_in == false){
					this.$emit('change_activity_to_refer_to', this.activity);

					this.$emit('show_auth_modal', true);
					return 0;

				}

				if (this.chosenOption  == 0) { //if no option has been chosen
					alert('Select an option');
					return 0;
				}

				this.activity.totalVotes += 1;
				this.activity.userHasVoted = true;

				for (var i = 0; i < this.activity.options.length; i++){
					if (this.activity.options[i].id  == this.chosenOption){
						this.activity.options[i].score += 1;
						break;
					}
				}
                
				var pollID = this.activity.id;
				axios.post(siteUrl + '/vote/',{
					poll_id: pollID, 
					option_id: vm.chosenOption,
				}).then(function(response){

				}).catch(function(error){
					vm.userHasVoted = false;
				})
			},

			comment: function(){
				if (this.user_logged_in == false){
					this.$emit('change_activity_to_refer_to', this.activity);
					this.$emit('show_auth_modal', true);
					return 0;
				}
			},

			seeResults: function(){
				var vm = this;
				var result = true;
				
				if (this.user_logged_in == false){
					this.$emit('change_activity_to_refer_to', this.activity);					
					this.$emit('show_auth_modal', result);
					return 0;
				}

					axios.post(siteUrl + '/viewresults',{
						poll_id: this.activity.id,
					}).then(function(response){
						vm.seenPollResults = true;
					}).catch(function(error){
						vm.seenPollResults = false;

				});

				
				
			},
			getPollMetrics(){
				var main_focus = this.activity.main_focus;
				var sub_focus = this.activity.sub_focus;

				if (main_focus == 'gender'){
					var labels = ['Male', 'Female'];
					var data = [this.activity['M'].votes, this.activity['F'].votes];

					this.makePieChart(labels, data);
				}

				else if (main_focus == 'age_range'){
					var ages = [];
					var i = parseInt(this.activity.lowerBound); 
					var upperBound = parseInt(this.activity.upperBound) + 1;
					while (i < upperBound){
						ages.push(i);
						i++;
					}
					var data = [];
					var age_vote = 0; 

					var labels = ["some"];
					ages.forEach(age=>{
						age_vote += parseInt(this.activity[age].votes);
					});

					data.push(age_vote);

					this.makePieChart(labels, data);
				}

			},

               makePieChart(aLabels, aData){
                    //destroy a previous chart
                    
                    var ctx = document.getElementById('metricsChart' + this.activity.id).getContext('2d');


                    var options = {
                        legend:{
                            display: true, 
                            position: "bottom",
                            labels:{
                                fontColor: '#333',
                                fontSize: 13
                            }
                        }
                    };
                    var data = {
                        labels: aLabels,
                        datasets: [
                            {
                                data: aData, 
                                backgroundColor: [
									"#00796B",
									'orange',
									"#C62828",
									"#8D6E63",
									"#8BC34A",
									"#26A69A",
									'#BF360C',
									"green",
									"#1565C0",
                            
                                ],
                                borderColor: [
									"#00796B",
									"orange",
									"#C62828",
									"#8D6E63",
									"#8BC34A",
									"#26A69A",
									'#BF360C',
									"green",
                                    "#1565C0",
                                ]
                            }
                        ]
                    };

                        
                        
                        chart1 = new Chart(ctx, {
                        type: "pie",
                        data: data,
                        options: options
                    });

                },

		},

		computed:{

			userHasVoted(){
				return this.activity.userHasVoted;
			},

			contextImageHeight(){
				var contextImage =	document.getElementById('opinionContextImage');
				var width = contextImage.style.width;
				
				contextImage.style.height = width;
			},


			totalVotes(){
				return this.activity.totalVotes;
			},

			activityIsAlreadyLiked(){
				
				return this.activity.userHasLiked;
			},

			numOfLikes(){
				return this.activity.numOfLikes;
			},

			calculatedScores(){
				if(this.activity.totalVotes ==0){
					return this.activity.options.map(a=>{
						a.percent = '0%'
						return a
					})
			}
				return this.activity.options.filter(a=>{
                    if (!isNaN(a.score) && a.score > 0){
                        a.percent = ( Math.round( (parseInt(a.score)/this.activity.totalVotes ) * 100) ) + '%'
					}
					else{
                        a.percent =  '0%'
					}
                    return a
                })
		},



	
		}	

	}

</script>