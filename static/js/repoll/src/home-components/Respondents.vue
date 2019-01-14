	<template id='respondents-template'>
		<transition name='modal'>
			<div class="modal-mask" v-show='show_respondents_modal'>
				<div class="modal-container">
					<div class="modal-header">


					</div>
					<div class="modal-body">
						<div class="card" v-for='respondent in respondents'>
							<img v-if='respondent.userPic' :src='userPic'/>
								<p>{{respondent.userFullName}}</p>
								<p>{{respondent.userName}}</p>
							<button> Follow</button>

						</div>
					</div>
				</div>
			</div>
		
		</transition>
	</template>


<script>
	var siteUrl = 'http://localhost:6543'

	export default {
		name: 'Respondents', 
		props: ['show_respondents_modal', 'activity'],

		data(){
			return{	
				respondents: [],
			}
		},
		watch:{
			show_respondents_modal: function(val){
				if (val == true){
					axios.get(siteUrl + '/voters/' + this.activity.id, {

					}).then(response=>{
					this.respondents = response.data;
					});
				}
			},
		},

		
	}

</script>