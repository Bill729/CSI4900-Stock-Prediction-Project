<template v-slot="">
  <nav class="navbar navbar-expand-lg navbar-absolute"
       :class="{'bg-white': showMenu, 'navbar-transparent': !showMenu}">
    <div class="container-fluid">
      <div class="navbar-wrapper">
        <a class="navbar-brand" href="#pablo">{{routeName}}</a>
      </div>
      <button class="navbar-toggler" type="button"
              @click="toggleMenu"
              data-toggle="collapse"
              data-target="#navigation"
              aria-controls="navigation-index"
              aria-label="Toggle navigation">
        <span class="navbar-toggler-bar navbar-kebab"></span>
        <span class="navbar-toggler-bar navbar-kebab"></span>
        <span class="navbar-toggler-bar navbar-kebab"></span>
      </button>
      <collapse-transition>
        <div id="menu" class="collapse navbar-collapse show" v-show="showMenu">
          <ul class="navbar-nav" :class="$rtl.isRTL ? 'mr-auto' : 'ml-auto'">
            <div class="input-group">
              <button class="btn btn-link" id="search-button">
                <a href="#/dashboard" class="router-link">
                  <i class="option-icon tim-icons icon-chart-pie-36"></i>
                  <span class="option-text">Dashboard</span>
                </a>
              </button>
            </div>
            <div class="input-group">
              <button class="btn btn-link" id="search-button">
                <a href="#/news" class="router-link">
                  <i class="option-icon tim-icons icon-single-copy-04"></i>
                  <span class="option-text">News</span>
                </a>
              </button>
            </div>
            <div class="input-group">
              <!-- <input type="text" class="form-control" placeholder="Search...">
              <div class="input-group-addon"><i class="tim-icons icon-zoom-split"></i></div> -->
              <button class="btn btn-link" id="search-button" data-toggle="modal" data-target="#searchModal" @click="focusOnSearchInput">
                <i class="option-icon tim-icons icon-zoom-split"></i>
                <span class="option-text">Search</span>
              </button>
              <!-- You can choose types of search input -->
            </div>
            <modal :show.sync="searchModalVisible"
                   class="modal-search"
                   id="searchModal"
                   :centered="false"
                   :show-close="true">
              <input slot="header"  ref="searchInput" v-model="searchQuery" type="text" class="form-control" id="inlineFormInputGroup" placeholder="SEARCH or TYPE 'ALL' for all tickers">
              <ul id="ul-ticker">
                <li class="li-ticker" v-for="ticker in tickers" :key="ticker">
                  <button @click="changeSelectedTicker(ticker);" v-if="searchQuery.toUpperCase() == 'ALL' || searchQuery != '' && ticker.toUpperCase().includes(searchQuery.toUpperCase())" class="btn btn-secondary active">
                    {{ ticker }}
                  </button>
                </li>
              </ul>
            </modal>
          </ul>
        </div>
      </collapse-transition>
    </div>
  </nav>
</template>
<script>
  import { CollapseTransition } from 'vue2-transitions';
  import Modal from '@/components/Modal';
  import axios from 'axios';

  export default {
    components: {
      CollapseTransition,
      Modal
    },
    computed: {
      routeName() {
        const { name } = this.$route;
        return this.capitalizeFirstLetter(name);
      },
      isRTL() {
        return this.$rtl.isRTL;
      }
    },
    data() {
      return {
        activeNotifications: false,
        showMenu: false,
        searchModalVisible: false,
        searchQuery: '',
        tickers: []
      };
    },
    methods: {
      capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
      },
      toggleNotificationDropDown() {
        this.activeNotifications = !this.activeNotifications;
      },
      getTickers(){
        const uri = 'http://127.0.0.1:5000/tickers';
        axios.get(uri)
        .then((res) => {
          console.log(res);
          this.tickers = res.data;
          return res.data;
        })
        .catch((error) => {
          console.error(error);
        });
      },
      closeDropDown() {
        this.activeNotifications = false;
      },
      toggleSidebar() {
        this.$sidebar.displaySidebar(!this.$sidebar.showSidebar);
      },
      hideSidebar() {
        this.$sidebar.displaySidebar(false);
      },
      toggleMenu() {
        this.showMenu = !this.showMenu;
      },
      focusOnSearchInput() {
        this.searchModalVisible = true;
        this.$nextTick(() => {
          this.$refs.searchInput.focus(); // Focus on the input field
        });
      },
      async changeSelectedTicker(ticker) {

        this.searchQuery = '';
        this.searchModalVisible = false;

        this.$nextTick(() => {
          this.$refs.searchInput.focus(); // Focus on the input field
        });

        await this.$store.dispatch("changeSelectedTicker", { name: ticker });
        await this.$store.dispatch('changeSelectedStockSymbol', ticker);


        this.$emit('stockSelected', ticker);
        
      }
    },
    mounted(){
      this.getTickers();
    }
  };
</script>
<style>
.router-link, .btn{
  display: flex !important;
  flex-direction: row !important;
  justify-content: center;
  text-decoration: none;
  color: white;
}
#search-button{
  color: white !important;
}
.router-link:hover, #search-button:hover{
  color: lightgray !important;
}
.router-link:focus{
  color: none;
}
.option-icon{
  margin-right: 0.35rem;
}
.btn-link{
  font-weight: 100 !important;
}
.input-group{
  margin: 0 !important;
}
</style>