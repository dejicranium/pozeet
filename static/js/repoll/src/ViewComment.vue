<template>
    <div id="view-comment-container">
		<div class='feed-container'>
			<div class="feed-card">
				<div class="avatar">
                     <img v-if='!comment.userPic' src="https://www.w3schools.com/howto/img_avatar.png"/>
					 <img v-else :src='comment.userPic'>
                </div>

               <div class="beside-avatar-box">
                    <div class="author-details">
                        <p class="name" style='font-weight:bold;'>{{comment.userName}}</p>
                        <p class="username"></p>
                        <p class="action"></p>
                    </div>


                    <h2 class="chosen-option">{{comment.optionChosen}}</h2>
                    <p class="comment" style='white-space:;'>{{comment.comment}}</p>


                    <div>
                        <div class="comment-question" v-if='comment.poll' tab-index="0">
                            <p class='author-name' style='font-weight:normal; color:teal;'>Poll</p>
                            <p class='author-name' style='font-size:bold;'>{{comment.poll.userName}} <span style="color:lightgray; font-weight:normal;">{{comment.poll.timeAdded}}</span></p>
							<p class='question'>{{comment.poll.question}}</p>


                        </div>
                            
							
						<div class="comment-question" v-else-if='comment.opinion' tab-index="0">
                            <p class='author-name' style='font-weight:normal; color:teal;'>Opinion</p>
                            <p class='author-name' style='font-size:bold;'>{{comment.opinion.userName}} <span style="color:lightgray; font-weight:normal;">{{comment.opinion.timeAdded}}</span></p>
							<p class='question'>{{comment.opinion.opinion}}</p>


                        </div>

                    </div>

					<div v-if="comment.opinion">
						<button @click='reply'> <i class="fas fa-reply button-icon"></i>Reply </button>
						<button @click=''><i class="far fa-thumbs-up button-icon"></i>Like</button>
						<!--<button @click="share"><i class="far fa-share-square button-icon"></i>Share</button> -->
					</div>
				</div>

            </div>

			<div class='addCommentBox' v-show="intent == 'toReply'">
				<form id='comment-form'>
					<textarea type="text" placeholder='Reply' v-model='replyText' @click="autoResize" name='reply' id='comment-form'></textarea>
					<button @click='replyComment'>Reply</button>
				</form>
			</div>

			<div class='other-details'>
				<div id='innerReply'>
					<comment v-for='reply in replies' :reply='reply'>
					</comment>

				</div>
            </div>
        </div>
    </div>
</template>

<script>
import ConvoComment from './view-converstation-components/ConvoComment.vue';
import axios from 'axios';

var siteUrl = "http://localhost:6543";
var commentId = document.getElementById('commentId').innerHTML;

var showSnackbar = function(text){
	var snackbar = document.getElementById('snackbar');
	snackbar.innerHTML = text;

    snackbar.className = "show";

    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ snackbar.className = snackbar.className.replace("show", ""); }, 4000);

}

export default {
    name: 'ViewComment',
    components:{
        'comment': ConvoComment,
    },
        data(){
			return{
            	some: 'deji',
				loading: '',
            	comment: {}, //it'a list because we want it to be reactive.
				chosenOption: 0,
				user_logged_in: false,
				comments: [],
				replies: [], 
				replyText: '',
				activeTab: '*',
				tabs: [],
				isActiveClass: 'isActive',
				intent: '',
				canAgreeToComments: false, //this will make us know whether user can press agree on another comment
				commentToAgreeWith: 0, 
			}
             
        },


        methods:{

			autoResize(event){
				event.preventDefault();
				var textarea = event.target;
				textarea.addEventListener('input', function(){
					var currentHeight = textarea.offsetHeight;
					var scrollHeight = textarea.scrollHeight;
					if (scrollHeight > currentHeight){
						textarea.style.height = scrollHeight + 'px';
					}
				});
			},

            changeCommentData(id, value){
                this.$set(this.comment, id, value);
            },


			reply(){
				if (this.user_logged_in == false){
					return 0;
					
				}

				if (this.intent == 'toReply'){
					this.intent = '';
				}
				else{
					this.intent = 'toReply';
				}

			},

			replyComment(event){
				event.preventDefault();
				var replyButton = event.target;
				replyButton.disabled = true;
				var vm = this;

				axios.post(siteUrl + '/reply-comment', {
					comment_id: vm.comment.id, 
					reply: vm.replyText,
				}).then(response=>{
					replyButton.disabled = false;
					vm.replyText = '';
					showSnackbar('Reply Added!');
					vm.intent = '';
					window.location.reload();
				}).catch(error=>{
					replyButton.disabled = false;
				});

			},	


		},

        created(){
           var vm = this;
            axios.get(siteUrl + '/get_comment/' + commentId)
            .then(function(response){
				vm.user_logged_in = response.data.user_logged_in;
				vm.changeCommentData('optionChosen', response.data.optionChosen);
                vm.changeCommentData('userName', response.data.userName);
				vm.changeCommentData('comment', response.data.comment);
                vm.changeCommentData('type', response.data.type);
                vm.changeCommentData('id', response.data.id);
                vm.changeCommentData('userPic', response.data.userPic);
				vm.changeCommentData('numOfShares', response.data.numOfShares);
                vm.changeCommentData('numOfAgrees', response.data.numOfAgrees);
                vm.changeCommentData('hasSharedComment', response.data.hasSharedComment);
				vm.changeCommentData('timeAdded', response.data.timeAdded);
				vm.changeCommentData('userIsFollowing', response.data.userIsFollowing);
				vm.changeCommentData('poll', response.data.poll);
				vm.changeCommentData('opinion', response.data.opinion);


				vm.loading = false;
				//should users be allowed to agree to a comment?
				//it all starts from knowing whether they have voted before.
				
            }).catch(function(error){
				vm.loading =false;
			    }
            
            );


			axios.get(siteUrl + '/replies/comment_id=' + commentId).then(response=>{
				this.replies = response.data.replies;
			});
        },
  
}
</script>
