<template>
  <div style="min-width: auto; min-height: auto; display: grid; grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));">
    <div class="news-item" v-for="newsItem in news" :key="newsItem.url">
      <div class="img-section">
        <a :href="newsItem.url">
          <img :src="newsItem.urlToImage" :alt="'Photo of article titled: ' + newsItem.title" />
        </a>
      </div>
      <div id="text-section">
        <a :href="newsItem.url">
          <h4 class="card-title">{{ newsItem.title }}</h4>
        </a>
        <h5 class="card-title">Published on {{ newsItem.publishedAt.replace('T', ' ').replace('Z', ' ') }}</h5>
        <h5 class="card-title">Published by {{ newsItem.author }}</h5>
        <h6 class="card-category">From {{ newsItem.source }}</h6>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'News',
  data(){
    return{
      news: []
    }
  },
  mounted() {
    this.fillNews();
    console.log(this.news);
  },
  methods: {
    async fillNews() {
      try{
        const response = await axios.get(`http://127.0.0.1:5000/stock/${this.$store.getters.getSelectedTickerData().name}/news`);
        this.news = response.data;
      }
      catch (error){
        console.error('Error fetching data:', error);
      }
    },
  }, 
};
</script>

<style>
img{
  object-fit: cover;
  width: 100%;
  height: 100%;
}
.img-section{
  width: 500px;
  height: 500px;
}
</style>