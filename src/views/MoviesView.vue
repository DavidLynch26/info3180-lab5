<template>
    <h1>Movies</h1>
    <div class="card-deck">
        <div v-for="movie in movies['movies']" class="card"  style="width: 18rem;">
            <img :src="movie['poster']" alt="" class="card-img-top">
            <div class="card-body">
                <h5 class="card-title">{{ movie['title'] }}</h5>
                <p class="card-text">{{ movie['description'] }}</p>
                <!-- <a href="" class="btn btn-primary"></a> -->
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted } from "vue";

    onMounted(() =>{
        fetchMovies();
    });

    const movies = ref([]);

    function fetchMovies() {
        fetch("/api/v1/movies", {
        method: 'GET',
        }) 
        .then(function (response) { 
            return response.json(); 
        })
        .then(function (data) { 
            // display a success message 
            console.log(data);
            movies.value = data;
            console.log(movies.value);
        })
        .catch(function (error) { 
            console.log(error); 
        });
    }
</script>