<template>
    <div>
        
        <div class="container" :v-for="user in users" :user='user'>
            <div class="image-container">
               <img class="user-image" src="user.userPic"/>
            </div>

            <div class="user-details-container">
                <p class='userFullName'>{{user.userFullName}} <br> <span class="username">{{user.username}}</span>
                    <br>
                    <span class="bio">
                        {{user.bio}}
                    </span>
                 </p>
            </div>

            <div class="follow-btn-container">
                <button>Follow</button>
            </div>

        </div>

    </div> 


</template>

<script>
export default {
    name: 'UsersModal',
    props: ['users']
}
</script>


<style scoped>
div{ 
    max-height: 50px;
    border: grey 0.5px solid;
    vertical-align: middle;
}
.container{ 
    background-color: whitesmoke;
    padding: 16px; 
    display: flex; 
    flex-direction: row; 
    -ms-flex-direction: row;
    

}
.image-container{
    margin-right: 5px;
    flex-basis: 25%;
}

.user-image{
    border-radius: 50%; 
    width: 18px; 
    height: 18px; 
    text-align: center;
}

.user-details-container{
    display: flex; 
    flex-direction: column;
    margin-right: 5px;
    -ms-flex-direction: column;
    flex-basis: 70%;
    

}

.userFullName{
    font-weight: bold; 
}

.username{
    font-weight: normal;
    color:bold;
    height: 15px; 
    margin: auto auto;
}

.follow-btn-container{
    
    flex-basis: 15%;
}

button{ 
    background-color: teal;
    border: 0;
    border-radius: 5px;
    color: white;
    text-align: center;
    height: 30px;
    margin: auto auto;
}

</style>

