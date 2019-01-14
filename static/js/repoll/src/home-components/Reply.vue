	<template>
		<transition name='modal'>
			<div class="modal-mask" v-show='show_reply_modal' @click='closeModal'>
				<div class="modal-container" @click.stop>
					<div class="modal-header">
						<p v-if="activity.type=='comment'">Replying to {{activity.commenter}}</p>

					</div>
					<div class="modal-body">
						<textarea v-model='replyText' @click='autoResize' style='height:100px; width:100%;'>


						</textarea>	
						<button @click='reply'><i class="fa fa-circle-o-notch fa-spin"></i> Reply</button>
					</div>
				
				
				</div>

			</div>
		
		</transition>
	</template>

    <script>

	//definitions
	var siteUrl = "http://localhost:6543";
	
	//importations
	import axios from 'axios';
	
    export default {
        name: 'Rely',
        props: ['show_reply_modal', 'activity'],
        data(){
            return {
                replyText: '',
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
			closeModal(){
				this.$emit('close_modal', false);

			},
			reply(event){
				
				var replyButton = event.target;
				replyButton.disabled = true;
				var vm = this;

				this.changeButtonContent(replyButton, '...');

				if (this.activity.type == 'comment'){
					axios.post(siteUrl + '/reply-comment', {
						comment_id: this.activity.id, 
						reply: this.replyText,
						
					}).then(response=>{
						vm.changeButtonContent(replyButton, "Reply");	
						replyButton.disabled = false;
						vm.closeModal();
						vm.replyText = '';
						vm.showSnackbar('Reply Added!');
				
					}).catch(error=>{
						vm.changeButtonContent(replyButton, "Reply");
						replyButton.disabled = false;
						vm.showSnackbar('Error Adding Reply');


					});

				}
				else{
					axios.post(siteUrl + '/reply-reply', {
						reply_id: this.activity.id, 
						reply: this.replyText,
					}).then(response=>{
						replyButton.disabled = false;
						vm.changeButtonContent(replyButton, 'Reply')
						vm.closeModal();
						vm.replyText = '';
									showSnackbar('Reply Added!');

					}).catch(error=>{
						replyButton.disabled = false;
						vm.changeButtonContent(replyButton, 'Reply');

						vm.showSnackbar('Error Adding Reply');

					});
		
				}
			
			},

		}

    }
    
    </script>


	<style>
	textarea{
		font-size: 12px;
	}
	</style>
	
    