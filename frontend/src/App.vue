<template>
  <div class="d-flex flex-column">
    <IndexPageNav />
    <div class="d-flex flex-column justify-content-center align-items-center">
      <router-view
        style="
          display: flex;
          flex-direction: column;
          justify-content: flex-start;
          align-items: center;
        "
      />
    </div>
  </div>
</template>
<script>
import IndexPageNav from "./components/LandingPage/IndexPageNav.vue";

export default {
  name: "IndexPageView2",
  components: {
    IndexPageNav,
  },
  mounted() {},
};
</script>

<style>
body,
html {
  height: 100%;
  margin: 0;
  padding: 0;
}
#app {
  min-height: 100vh;
  background-image: url("./../public/img/icons/original-025fe3b1ac70c873f433aec624a65bdd.gif");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
}
</style>
