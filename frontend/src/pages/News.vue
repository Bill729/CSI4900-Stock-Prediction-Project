<template>
  <div id="wrapper">
    <div class="news-item" v-for="newsItem in news" :key="newsItem.url">
      <div class="img-section">
        <a :href="newsItem.url">
          <img :src="newsItem.urlToImage" :alt="'Photo of article titled: ' + newsItem.title" />
        </a>
      </div>
      <div id="text-section">
        <a :href="newsItem.url" target="_blank">
          <h4 class="card-title">{{ newsItem.title }}</h4>
        </a>
        <h5 class="card-category">Published on {{ newsItem.publishedAt.replace('T', ' ').replace('Z', ' ') }}</h5>
        <h5 class="card-category">Published by {{ newsItem.author }}</h5>
        <h6 class="card-title">From {{ newsItem.source }}</h6>
        <button type="button" class="btn btn-primary">
          <a class="text-white font-weight-bold" :href="newsItem.url" target="_blank">Read</a>
        </button>
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
.card-title, .card-category{
  margin: 0;
}
.card-category:nth-child(3){
  margin-bottom: 1rem;
}
.card-title:nth-child(4){
  margin-bottom: 1rem;
}
h4.card-title{
  font-size: 2.5rem;
  margin: 0.75rem 0;
}
.card-title:nth-child(2){
  margin-bottom: 1rem;
}

button{
  margin-top: 0.5rem;
}
.img-section{
  width: 100%;
  height: 375px;
}
img{
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 0.75rem;
}
#wrapper{
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  padding: 2rem;
  grid-gap: 2rem;
  align-items: stretch;
  padding-bottom: 4rem;
}
@media screen and (max-width: 1600px  ){
  #wrapper{
    display: flex;
    flex-direction: column;
  }
  .news-item{
    margin: 0 auto;
    width: 100%;
    max-width: 1200px;
  }
}
.news-item{
  max-width: 850px;
  margin-top: 0;
  position: relative;
  padding-bottom: 4rem;
}
.news-item .btn{
  position: absolute;
  bottom: 0;
}
</style>