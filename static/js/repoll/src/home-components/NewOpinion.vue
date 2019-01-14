\<template id='new-opinion-template' type='x/template'>
	<transition name='modal'>
		<div class='modal-mask' v-show='show_opinion_modal' @click='closeModal'>
			<div class='modal-container' @click.stop >
				<div class='modal-header' style='color:black'>
					<h3>New opinion</h3>
				</div>
				
				<form id='opinion-form' enctype='multipart/form-data' method='post'>
				<div class='modal-body new-opinion-modal-body' style="width:100%; box-sizing:border-box; padding-bottom:20px; padding-right:0px; padding-left:0px; padding-top:0px;">
					<textarea style='width: 100%; height: 100px; border-radius:0px; font-size:13px; margin-bottom:5px;; ' v-model='opinion' id='comment-input' @click='autoResize' class='form-control final-input' name='comment' form='comment-form' placeholder='Have your say'></textarea>
					
          		<label @click='addOpinionImage' id='opinion-image-label'style='background-color:lightgrey; display:inline-block; padding:5px; border-radius:5px; margin-left:10px;'>
				  <input type="file" style='display:none'
               		id="opinion-image" name="opinion-image"
					
               		accept="image/png, image/jpeg" />
					<span><i class="far fa-image button-icon" ></i>Add image</span>
					<img id='opinion-image-display'></img>					

				</label><br>

				<button type='button' id='createOpinionButton' style='margin-bottom: 10px; border-radius:10px; margin-left:10px;margin-right:10px;' @click='createOpinion'>  <i class="fa fa-circle-o-notch fa-spin" v-if=''></i>Share</button>
				</div> 

				</form>

			</div> 

		</div>
	</transition>
</template>


<script>
	var siteUrl = 'http://localhost:6543';

	import axios from 'axios';
	export default {
		name: 'NewOpinion',
		props: ['show_opinion_modal'],

		data(){
			return{
				opinion: '',
				newOpinionObject: {},
 			}
		},

		mounted(){
		
		},

		methods:{

			addOpinionImage(){
				var opinionImageInput = document.getElementById('opinion-image');
				var opinionImageDisplay = document.getElementById('opinion-image-display');
				var opinionImageInputLabel = document.getElementById('opinion-image-label');
				var opinionImageInputHeight = opinionImageInputLabel.clientHeight;

				opinionImageInput.addEventListener('input', function(){
					var imageFiles = opinionImageInput.files;
					var neededFile = imageFiles[0];
					opinionImageDisplay.style.height = '20px';
					opinionImageDisplay.style.width = '20px';
					opinionImageDisplay.src = window.URL.createObjectURL(neededFile);
				});
		},


			createOpinion(event){
				var vm = this;
				/**var target = event.target;
				event.target.innerHTML = '...';
				target.disabled = true;
				axios.post(siteUrl + '/new/opinion',{
					opinion: vm.opinion,
			
			
				}).then(function(response){
					vm.opinion = '';
					target.innerHTML = 'Share';
					target.disabled = false;

			**/

					var form = document.getElementById('opinion-form');
					event.target.disabled = true;
					var formData = new FormData(form);
					formData.append('opinion', vm.opinion);
					var request = new XMLHttpRequest();
				
					vm.changeButtonContent(event.target, '...');

					request.open("POST", siteUrl + '/new/opinion');
					request.onreadystatechange = function(){
						if (request.readyState == XMLHttpRequest.DONE){
							if(request.status == 200){
								vm.closeModal();
								vm.showSnackbar('Opinion published!');
								vm.changeButtonContent(event.target, 'Share');
								event.target.disabled = false;
							}
							else {
								vm.showSnackbar('There was an error sharing your opinion. Please Retry');
								vm.changeButtonContent(event.target, 'Share');
								event.target.disabled = false;

							}	
					
						}
					}
				
					request.send(formData);
				},
		

	
	
			closeModal(){
				this.$emit('close_new_opinion_modal', true);

			},

			alterObject(key, value){
				this.$set(this.newOpinionObject, key, value);
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

			addToActivities(){
				this.$emit('act_add_to_activities', this.newOpinionObject);
			},


		},		
	}
</script>

<style scoped>
	.modal-container .modal-body{
		position: relative;
		padding-bottom: 20px;
	}

	.modal-container .modal-body .final-input{
	}
	.modal-container .modal-body button{
		position: absolute;
		right: 0; 
		bottom: 0;
		margin-right: 20px; 
	}


</style>
