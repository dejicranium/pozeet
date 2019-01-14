	<template id='comment-template'>
		<div class='comment-card'>
			<div class='avatar'>
                <img v-if='comment.userPic == null'src="https://www.w3schools.com/howto/img_avatar.png"/>
			    <img v-else :src="comment.userPic"/>

			</div>

			<div class='beside-avatar-box'>
				<div class='author-details'>
					<h3 class='name' style='font-weight:bold'>{{comment.userName}}</h3>
					<p class='name' style='color:lightgray'>{{comment.timeAdded}}</p>

				</div> 

				<div class='chosen-option'>
					<h4 class='option'>{{comment.option}}</h4>
				</div>

				<div class='reason' id=''>
					<p>{{comment.comment}}</p>
				</div>
				
				<div class='action-buttons'> 
					<button v-if='can_agree_to_comments' @click='agree'>Agree<span>{{numOfAgrees}}</span></button> 
					<button v-else style='background-color:transparent;'><span style='color:black; font-weight:bold;'>{{comment.numOfAgrees}} Agrees </span></button> 
					<button @click='share' v-if='!hasSharedComment'>Share {{numOfShares}} </button>
					<button v-else style='background-color:transparent;'><span style='color:black; font-weight:bold;'>{{numOfShares}} Shares </span></button> 
				</div>

            </div>


			</div>

	</template>


<script>
	import axios from 'axios';
    var siteUrl = "http://localhost:6543";
    export default {
        name: 'Comment', 
		props: ['comment', 'can_agree_to_comments'],
 
		data(){
			return {
				canAgreeToComments: this.can_agree_to_comments,
				replies: this.comment.replies,
				hasSharedComment: this.comment.hasSharedComment,
				numOfAgrees: this.comment.numOfAgrees,
				numOfShares: this.comment.numOfShares,
			}
		}, 

		methods:{
			share(){
				var vm = this;
				axios.post(siteUrl+'/share/', {
					comment_id: vm.comment.id,
					
				}).then(response=>{
					vm.hasSharedComment = true;
					vm.numOfShares += 1;
				}).catch(error=>{
					vm.hasSharedComment = false;
				});

			},
			
			agree(){
				var vm = this;
				axios.post('http://localhost:6543/agree',{
					comment_id: this.comment.id,
					option_id: this.comment.optionId,
					poll_id: this.comment.poll_id,
				}).then(function(response){
					vm.numOfAgrees+=1;
					vm.setCannotAgree();
				}).catch(function(response){

				});
			},

			setCannotAgree(){
				var option_voted_for = this.comment_optionId;
				vm.$emit('change_can_agree_state', option_voted_for);

			},
		},


    }

</script>
