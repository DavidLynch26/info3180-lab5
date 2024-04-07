<template>
    <div v-if="msg != null">
        <div v-if="msg['errors']" class="alert alert-danger" role="alert">
            <li v-for="err in msg['errors']"> {{ err }} </li>
        </div>
        <div v-else class="alert alert-success" role="alert">
            <p>{{ msg['message'] }}</p>
        </div>
    </div>
    <form @submit.prevent="saveMovie" id="movieForm">
        <div class="form-group mb-3">
            <label for="title" class="form-label">Title</label>
            <input type="text" id = "title" name="title" class="form-control">
        </div>
        <div class="form-group mb-3">
            <label for="description" class="form-label">Description</label>
            <input type="text" id="description" name="description" class="form-control">
        </div>
        <div class="form-group mb-3">
            <label for="poster" class="form-label">Poster</label>
            <input type="file" id="poster" name="poster" class="form-control">
        </div>
        <button class="btn btn-primary" type="submit">Submit</button>
    </form>
</template>

<script setup>
    import { ref, onMounted } from "vue";

    onMounted(() =>{
        getCsrfToken();
    });
    
    const msg = ref(null);
    let csrf_token = ref("");

    function getCsrfToken() {
        fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            csrf_token.value = data.csrf_token;
        })
    }

    function saveMovie() {
        let movieForm = document.getElementById('movieForm');
        let form_data = new FormData(movieForm);

        fetch("/api/v1/movies", {
        method: 'POST',
        body: form_data,
        headers: {
            'X-CSRFToken': csrf_token.value
        }
        }) 
        .then(function (response) { 
            return response.json(); 
        })
        .then(function (data) { 
            // display a success message 
            console.log(data);
            msg.value = data;
        })
        .catch(function (error) { 
            console.log(error); 
        });
    }
</script>