<template type='x/template' id='add-comment-template'>
	<transition name='modal'>
	<div class="modal-mask" id='add-comment-modal' v-show='show_comment_modal' @click='closeModal'>
		<div class="modal-container" @click.stop>
			<div class='modal-header'>
				<span class='close-mark'> x </span>
				<h3>Commenting on:</h3>
				<h5 v-if='activity.question'>{{activity.question}}</h5>
				<h5 v-else>{{activity.opinion}}</h5>
			</div>
			<div class='modal-body'>
				<form id='comment-form'>
					<p class='chosen'>{{chosenOptionTitle}}</p>
					<textarea id='comment-input' @click='autoResize' class='form-control' name='comment' form='comment-form' placeholder='Reason'></textarea>
				
				<div class="grouped-buttons">
					<button @click='comment' id='addCommentButton'> <i class="fa fa-circle-o-notch fa-spin"></i>Comment</button>
					<button v-if='activity.opinion' style='margin-right:10px;' @click='comment'><i class="fa fa-circle-o-notch fa-spin"></i>Skip</button>
				</div>
				</form>
			</div>
		</div>
	</div>
	</transition>

</template>


<script>
	import axios from 'axios';
	var siteUrl = 'http://localhost:6543';
	
	export default {
		name: 'AddComment',
		props: ['show_comment_modal', 'activity', 'option'],
		computed:{
			chosenOptionTitle(){
				if (this.activity){
					for (let i = 0; i < this.activity.options.length; i++){
						if (this.activity.options[i].id == this.option){
							return this.activity.options[i].option;
						}
					}

				}
			},

			agreeOrDisagree(){
				return this.option;
			},
		},

		methods: {
			comment(event){
				var vm = this;
				var form = document.getElementById('comment-form');
				event.preventDefault();
				document.getElementById('addCommentButton').disabled = true;
				var formData = new FormData(form);
				this.changeButtonContent(event.target, '...');
				
				if (this.activity.type=='poll'){
					var vm = this;

					formData.append('poll_id', this.activity.id);
					formData.append('option_id', this.option);
					var request = new XMLHttpRequest();
					request.open("POST", siteUrl + '/comment/');
					request.onreadystatechange == function(){
						if (request.readyState == XMLHttpRequest.DONE){
							if (request.status == 200){
								vm.$emit('activity_voted', [vm.activity.id, vm.option, vm.activity.type]);
								vm.closeModal();
								vm.showSnackbar("Comment added!");
								vm.changeButtonContent(event.target, 'Comment');
								document.getElementById('addCommentButton').disabled = false;

							}


							else{

								vm.showSnackbar("An error occured while adding your comment");
								document.getElementById('addCommentButton').disabled = false;
								vm.changeButtonContent(event.target, 'Comment');

							}
						}
					}
					request.send(formData);
				}
				else {
					var vm = this;
					formData.append('opinion_id', vm.activity.id);
					formData.append('option_id', vm.option);
					var request = new XMLHttpRequest();
					request.open("POST", siteUrl + '/comment/');
					request.onreadystatechange = function(){
						if (request.readyState == XMLHttpRequest.DONE){
							if (request.status == 200){
								vm.closeModal();
								vm.showSnackbar("Comment Added");
								vm.changeButtonContent(event.target, 'Comment');
								vm.$emit('activity_voted', [vm.activity.id, vm.option, vm.activity.type]);
								document.getElementById('addCommentButton').disabled = false;

								//window.location.reload();
							}


							else{
								document.getElementById('addCommentButton').disabled = false;
								vm.changeButtonContent(event.target, 'Comment');
							}
						}
					}
					request.send(formData);					
				}
			},

			closeModal(){		
				this.$emit('close_add_coment_modal', false);
				this.option = null;
			},

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

			created(){
			
			},
		},

	}


</script>

<style scoped>
	#comment-form{
		margin-bottom: 30px;
	}
	.modal-body {
		position: relative;
		padding: 10px 0px 40px 0px;
	}

</style>
