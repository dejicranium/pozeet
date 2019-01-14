<template id="notification-template">
    <div>
            <div class="notification-card" v-for="notification in notifications" :notification="notification">
                <p v-html="notification.text"></p>
            </div>

    </div>
</template>


<script>
import vue from 'vue';
import axios from 'axios';

var userId = document.getElementById('user-id-signifier').innerHTML;
var siteUrl = "http://a78f522e.ngrok.io";

export default {
    name: 'Notification', 
    data(){
        return {
            notifications: [],
            unseenNotifications: [],
        }
    },
    
    methods: {

        flattenUnseenNotifications(){
            this.unseenNotifications = this.unseenNotifications.join(",");
            
        },
        getNotifications(){
            var vm = this;
            axios.get(siteUrl + '/notifs/' + userId).then(response=>{
                vm.notifications = response.data.notifs;
                vm.unseenNotifications = response.data.unseenNotifs;
                

                if (vm.unseenNotifications != []){
                    vm.flattenUnseenNotifications();
                
                    axios.post(siteUrl + '/mark-as-seen', {
                        notifications: vm.unseenNotifications,
                    });
                }
            });

        },

        markNotificationsAsSeen(){
            this.flattenUnseenNotifications();
            alert(this.unseenNotifications);
            var vm = this;

        }
    },

    created(){
        this.getNotifications();
    },

    


}
</script>


<style scoped>

    .notification-card{
        background-color:white;
        padding: 30px 16px;        
        box-shadow: lightgrey 1px;
        border-radius: 2px;
        border: 0.3px solid lightgray;
        font-size: 14px;
        margin-bottom:2px;

    }
</style>






