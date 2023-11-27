<template>
  <div>
    <div class="news-item" v-for="newsItem in news" :key="newsItem.url" @click="">
      <a :href="newsItem.url">
        <img :src="newsItem.urlToImage" :alt="'Photo of article titled: ' + newsItem.title" />
      </a>
      <div id="text-section">
        <h1 class="card-title">{{ newsItem.title }}</h1>
        <h4 class="card-title">Published on {{ newsItem.publishedAt.replace('T', ' ').replace('Z', ' ') }}</h4>
        <h4 class="card-title">Published by {{ newsItem.author }}</h4>
        <h3 class="card-category">Source: {{ newsItem.source }}</h3>
        <p>
          Lorem, ipsum dolor sit amet consectetur adipisicing elit. Possimus autem blanditiis fugiat aspernatur quae saepe vel non. Nam, excepturi maxime esse minima et ad voluptatibus!
        </p>
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
.news-item{
  display: flex;
  margin: 0 auto;
  width: 90%;
  margin-bottom: 3rem;

  & > #text-section{
    padding-left: 1.5rem;
    & > *{
      padding: 0;
      margin: 1rem 0;
    }
  }

  & > *{
    height: 40%;
  }

  & > a{
    display: block;
    width: 40%;
    & > img{
      width: 100%;
    }
  }
}
</style>